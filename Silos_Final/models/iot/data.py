from models.db import db
from models.iot.devices import Device
from datetime import datetime

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=True)

    def save_data(device_id, value):
        device = Device.get_device_by_id(device_id)
        if device and device.is_active:
            data = Data(device_id=device_id, value=value, timestamp = datetime.now())
            db.session.add(data)
            db.session.commit()
    
    def get_latest_data_for_device(device_id):
        return Data.query.filter_by(device_id=device_id).order_by(Data.timestamp.desc()).first()
    
    def get_data_for_device_in_range(device_id, start_time, end_time):
        return Data.query.filter(
            Data.device_id == device_id,
            Data.timestamp >= start_time,
            Data.timestamp <= end_time
            ).order_by(Data.timestamp).all()
    