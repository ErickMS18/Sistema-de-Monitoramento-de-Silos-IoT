from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models.db import db
from models.users_db import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login_post', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user)

    return redirect(url_for('home'))

@auth.route('/login_role')
def login_role():
    return render_template('login_role.html')

@auth.route('/login_role', methods=['POST'])
def login_role_post():
    name = request.form.get('name')
    password = request.form.get('password')

    if not name:
        return redirect(url_for('auth.login_role'))  

    user = User.query.filter_by(name=name).first()

    if user:
        return redirect(url_for('auth.login_role'))

    new_user = User(name=name, password=generate_password_hash(password), role=1)  
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))