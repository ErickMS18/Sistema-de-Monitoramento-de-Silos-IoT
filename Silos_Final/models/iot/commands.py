from models.db import db
from models.iot.devices import Device
from datetime import datetime

class Command(db.Model):
    __tablename__ = 'command'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100))
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def get_all_commands():
        return Command.query.all()
    
    def save_command(topic, message):
        command = Command(topic = topic, message = message, timestamp = datetime.now())
        db.session.add(command)
        db.session.commit()
