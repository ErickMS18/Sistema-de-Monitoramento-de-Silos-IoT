from flask import Flask
from models import *
from werkzeug.security import generate_password_hash

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()

        if not User.query.first():
            admin1 = User(name = 'admin1', password = generate_password_hash('123'), role = 1)
            erick = User(name = 'erick', password = generate_password_hash('123'), role = 2)
            ceci = User(name = 'ceci', password = generate_password_hash('123'), role = 3)
            teeny = User(name = 'teeny', password = generate_password_hash('123'), role = 1)

        db.session.add_all([admin1, erick, ceci, teeny])
        db.session.commit()
