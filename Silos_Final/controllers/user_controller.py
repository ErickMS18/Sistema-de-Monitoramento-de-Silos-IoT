from flask import Blueprint, request, render_template, redirect, flash, url_for
from models.users_db import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user


user = Blueprint("user", __name__, template_folder="views")

roles = {1: "admin", 2: "estatistico", 3: "operador"}

@user.route('/')
def pagina_login():
    return render_template("login.html")

@user.route('/page_users')
@login_required
def page_users():
    users = User.get_users()
    return render_template("users.html", users=users, user_role = current_user.role, roles = roles)

@user.route('/validated_user', methods=['POST'])
@login_required
def validar_login():
  
    usuario = request.form.get('user')
    senha = request.form.get('password')

    user = User.query.filter(User.name == usuario).first()

    if user is not None:
        if check_password_hash(user.password, senha):
            return render_template('home.html')
        else:
            flash("Senha inválida!")
            return redirect(url_for('user.pagina_login'))
    else:
        flash("Usuário não reconhecido!")
        return redirect(url_for('user.pagina_login'))
    

@user.route('/register_user')
@login_required
def register_user():
    return render_template("register_user.html")

@user.route('/add_user', methods=['GET','POST'])
@login_required
def add_user():
    name = request.form.get("name")
    password = request.form.get("password")
    password_hash = generate_password_hash(password)
    role = request.form.get("role")

    User.save_user(name, password_hash, role)

    users = User.get_users()

    return render_template("users.html", users=users, user_role = current_user.role, roles = roles)  

@user.route('/remove_user')
@login_required
def remove_user():
    users = User.get_users()
    return render_template("remove_user.html", users=users,user_role = current_user.role, roles = roles)

@user.route('/del_user', methods=['GET','POST'])
@login_required
def del_user():
    old_user_id = request.form.get('user')  
    user_id = int(old_user_id)   

    users = User.delete_user(user_id)

    return render_template("users.html", users=users, user_role = current_user.role, roles = roles)  

@user.route('/list_users')
@login_required
def list_users():
    users = User.get_users()
    return render_template("users.html", users=users, user_role = current_user.role, roles = roles)

@user.route('/update_user')
@login_required
def update_user():
    users = User.get_users()
    return render_template("update_user.html", users=users, user_role = current_user.role, roles = roles)

@user.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    old_user_id = request.form.get('old_user')  
    user_id = int(old_user_id)  
    
    new_username = request.form.get('new_username')
    new_password = request.form.get('new_password')
    new_password_hash = generate_password_hash(new_password)
    new_role = request.form.get('new_role')

    users = User.update_user(user_id, new_username, new_password_hash, new_role)
    
    return render_template("users.html", users=users, user_role = current_user.role, roles = roles)  