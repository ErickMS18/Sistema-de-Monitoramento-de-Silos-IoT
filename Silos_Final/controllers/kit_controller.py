from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models.iot.silo_kit import Kit
from models.db import db
from models.iot.devices import Device
from flask_login import login_required, current_user

kits = Blueprint('kits', __name__, template_folder='views')

@kits.route('/kits')
@login_required
def view_kits():
    kits = Kit.get_all_kits()
    return render_template('kits.html', kits=kits,user_role = current_user.role)

@kits.route('/kit/<int:kit_id>', methods=['GET', 'POST'])
@login_required
def view_kit(kit_id):
    kit = Kit.query.get_or_404(kit_id)

    if request.method == 'POST':
        name = request.form['name']
        device_type = request.form['device_type']
        unit = request.form['unit']
        is_active = 'is_active' in request.form
        Device.create_device(name, device_type, unit, is_active, kit_id)

    return render_template('view_kit.html', kit=kit,user_role = current_user.role)

@kits.route('/kit/create', methods=['GET', 'POST'])
@login_required
def create_kit():
    if request.method == 'POST':
        name = request.form.get('name')
        Kit.create_kit(name)
        return redirect(url_for('kit_bp.view_kits'))
    return render_template('kit_create.html',user_role = current_user.role)

@kits.route('/kits', methods=['GET', 'POST'])
@login_required
def manage_kits():
    if request.method == 'POST':
        name = request.form['name']
        Kit.create_kit(name)
    kits = Kit.get_all_kits()
    return render_template('kits.html', kits=kits,user_role = current_user.role)

@kits.route('/kits/delete/<int:kit_id>', methods=['POST'])
@login_required
def delete_kit(kit_id):
    Kit.delete_kit(kit_id)
    return redirect(url_for('kits.manage_kits'))

@kits.route('/kits/edit/<int:kit_id>', methods=['GET', 'POST'])
@login_required
def edit_kit(kit_id):
    if current_user.role != 1:  
        abort(403)
    
    kit = Kit.query.get_or_404(kit_id)
    
    if request.method == 'POST':
        kit.name = request.form['name']
        db.session.commit()
        flash('Kit atualizado com sucesso!', 'success')
        return redirect(url_for('kits.view_kits'))  
    
    return render_template('edit_kit.html', 
                         kit=kit,
                         user_role=current_user.role)




