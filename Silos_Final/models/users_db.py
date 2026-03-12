from models.db import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id= db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column('role', db.Integer, nullable=False) 


    def save_user(name, password, role):
        user = User(name = name, password = password, role = role)

        db.session.add(user)
        db.session.commit()

    
    def get_users():
        users = User.query.add_columns(User.id, User.name, User.role).all()
        return users
    
    def get_single_user(id):
        user = User.query.filter(User.id == id).first()

        if user is not None:
            user = User.query.filter(User.id == id).add_columns(User.id, User.name, User.password, User.role).first()
            
            return [user]
        
    def update_user(id, name, password, role):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            user.name = name
            user.password = generate_password_hash(password)
            user.role = role
            db.session.commit()

            return User.get_users()
        
    def delete_user(id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            
        return User.get_users()
