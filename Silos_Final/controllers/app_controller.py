from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash   
from models.db import db, instance
from models.iot.data import Data
from models.iot.devices import Device
from models.iot.commands import Command

from controllers.user_controller import user
from controllers.devices_controller import devices
from controllers.data_controller import data
from controllers.kit_controller import kits
from utils.auth import auth

from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from models.users_db import User
from flask_login import LoginManager, login_required, current_user, login_user

from datetime import datetime
import time
from collections import defaultdict, deque
import json

temperature = 0
humidity = 0
level = 0

def create_app():
    app = Flask(__name__, template_folder="./views/", static_folder="./static/", root_path="./")

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(devices, url_prefix='/')
    app.register_blueprint(data, url_prefix='/')
    app.register_blueprint(kits, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = '' 
    app.config['MQTT_PASSWORD'] = '' 
    app.config['MQTT_KEEPALIVE'] = 5000 
    app.config['MQTT_TLS_ENABLED'] = False 

    mqtt = Mqtt(app)

    mqtt_messages = {}

    subscribed_topics = ['silo_data']

    MAX_HISTORY = 10
    mqtt_messages = defaultdict(lambda: deque(maxlen=MAX_HISTORY))


    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
            for topic in subscribed_topics:
                client.subscribe(topic)
                print(f"Subscribed to topic: {topic}")
        else:
            print(f"Connection failed with code {rc}")

    @mqtt.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print(f"Disconnected with return code: {rc}")
        if rc != 0:
            print("Attempting to reconnect...")
            reconnect(client)

    def reconnect(client):
        delay = 1
        while True:
            try:
                client.reconnect()
                print("Reconnected successfully")
                return
            except Exception as e:
                print(f"Retry in {delay}s: {e}")
                time.sleep(delay)
                delay = min(delay * 2, 30)


    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        if message.topic in subscribed_topics:
            print(message.payload.decode())

            payload = json.loads(message.payload.decode())

            device_name = payload['device_name']
            value = payload['value']

            with app.app_context():
                device = Device.get_device_by_name(device_name)
                if device:
                    device_id = device.id
                    Data.save_data(device_id, value)
                else:
                    print(f"Device with name '{device_name}' not found in database.")


    @app.route('/publish/<topic>/<message>')
    def publish_message(topic, message):
        mqtt.publish(topic, message)
        return f"Published '{message}' to '{topic}'"

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    @app.route('/')
    def index():
        if current_user.is_authenticated: 
            return redirect(url_for('home'))  
        return redirect(url_for('login'))  

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template("login.html")

    @app.route('/login', methods=['POST'])
    def login_post():
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(name=name).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Usuário ou senha incorretos')
            return redirect(url_for('login'))
        
        # Verificação extra para garantir que é um User válido
        if not isinstance(user, User):
            flash('Erro no sistema de autenticação')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('home')) 

    @app.route('/home')
    @login_required
    def home():
        return render_template("home.html", user_role=current_user.role)

    @app.route('/remote_commands')
    @login_required
    def remote_commands():
        return render_template('remote_commands.html', user_role = current_user.role)
    
    @app.route('/projeto')
    def projeto():
        return render_template('projeto.html')

    @app.route('/send_message', methods=['GET', 'POST'])
    @login_required
    def send_message():
        if request.method == 'POST':
            topic = request.form.get('topic')
            message = request.form.get('message')

            if topic and message:
                mqtt.publish(topic, message)
                print(f"Message sent to {topic}: {message}")
                Command.save_command(topic, message)

        return render_template('remote_commands.html', user_role = current_user.role)
    
    @app.route('/command_history', methods=['GET', 'POST'])
    @login_required
    def command_history():
        history = Command.get_all_commands()
        return render_template('command_history.html', history = history, user_role = current_user.role)

    @app.route('/api/data')
    def get_mqtt_data():
        return {
            topic: list(messages)
            for topic, messages in mqtt_messages.items()
        }

    return app