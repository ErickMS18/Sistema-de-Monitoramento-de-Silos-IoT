from flask import Blueprint, request, render_template, jsonify
from models.iot.data import Data
from models.iot.devices import Device
from models.iot.silo_kit import Kit
from datetime import datetime
from flask_login import current_user


data = Blueprint("data",__name__, template_folder="views")

@data.route("/get_data/<int:device_id>", methods = ['GET', 'POST'])
def get_data(device_id):
    id = device_id
    start_str = request.form['start']
    end_str = request.form['end']

    start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
    end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")

    data = Data.get_data_for_device_in_range(id, start, end)
    device = Device.get_device_by_id(device_id)
    devices = Device.get_all_devices()
    return render_template("data.html", devices = devices, device = device, data = data, user_role = current_user.role)

@data.route('/data/<int:device_id>', methods=['GET', 'POST'])
def view_data(device_id):
    device = Device.query.get_or_404(device_id)
    data = None
    labels = []
    values = []

    if request.method == 'POST':
        start_str = request.form.get('start')
        end_str = request.form.get('end')

        if start_str and end_str:
            start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
            end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
            data = Data.get_data_for_device_in_range(device_id, start, end)

            labels = [d.timestamp.strftime('%Y-%m-%d %H:%M') for d in data]
            values = [d.value for d in data]

    return render_template('data.html', device=device, data=data, labels=labels, values=values, user_role=current_user.role, method=request.method)

@data.route('/view_rt_data')
def view_rt_data():
    return render_template('view_rt_data.html', user_role = current_user.role)

@data.route('/kits_overview_data')
def kits_overview_data():
    all_kits = Kit.query.all()
    
    kits_data = []
    
    for kit in all_kits:
        kit_info = {
            'id': kit.id,
            'name': kit.name,
            'devices': []
        }
        for device in kit.devices:
            latest_data = Data.get_latest_data_for_device(device.id)
            kit_info['devices'].append({
                'id': device.id,
                'name': device.name,
                'type': device.device_type,
                'unit': device.unit,
                'latest_data': {
                    'value': latest_data.value if latest_data else None,
                    'timestamp': str(latest_data.timestamp) if latest_data else None
                }
            })
        kits_data.append(kit_info)
    
    return jsonify(kits_data)