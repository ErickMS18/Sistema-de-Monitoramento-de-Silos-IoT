from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.devices import Device
from models.iot.silo_kit import Kit
from models.iot.data import Data
from models.db import db
from flask_login import login_required, current_user


devices = Blueprint("devices",__name__, template_folder="views")

@devices.route('/devices', methods=['GET', 'POST'])
@login_required
def manage_devices():
    kits = Kit.get_all_kits()
    if request.method == 'POST':
        name = request.form['name']
        device_type = request.form['device_type']
        unit = request.form['unit']
        is_active = 'is_active' in request.form
        kit_id = request.form['kit_id']
        Device.create_device(name, device_type, unit, is_active, kit_id)
    devices = Device.get_all_devices()
    return render_template('devices.html', devices=devices, kits=kits, user_role = current_user.role)

@devices.route('/devices/delete/<int:device_id>', methods=['POST'])
@login_required
def delete_device(device_id):
    device = Device.get_device_by_id(device_id)
    kit_id = device.kit_id
    Device.delete_device(device_id)
    return redirect(url_for('kits.view_kit', kit_id=kit_id))

@devices.route('/data/<int:device_id>')
@login_required
def view_data(device_id):
    device = Device.query.get(device_id)
    if device:
        data = Data.query.filter_by(device_id=device_id).all()
        return render_template('data.html', device=device, data=data, user_role = current_user.role)
    return "Device not found", 404


@devices.route('/devices/edit/<int:device_id>', methods=['GET', 'POST'])
@login_required
def edit_device(device_id):
    device = Device.query.get_or_404(device_id)
    kits = Kit.get_all_kits()
    if request.method == 'POST':
        name = request.form['name']
        device_type = request.form['device_type']
        unit = request.form['unit']
        is_active = 'is_active' in request.form
        kit_id = request.form['kit_id']

        id = device.id
        Device.edit_device(id, name, device_type, unit, is_active, kit_id)
        return redirect(url_for('kits.view_kit', kit_id=kit_id))
    return render_template('edit_device.html', device=device, kits=kits, user_role = current_user.role)




