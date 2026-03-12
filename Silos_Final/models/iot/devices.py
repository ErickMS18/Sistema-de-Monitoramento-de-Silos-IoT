from models.db import db

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(15), nullable=False)  # 'sensor', 'actuator'
    unit = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    
    kit_id = db.Column(db.Integer, db.ForeignKey('kits.id'), nullable=False)
    kit = db.relationship('Kit', back_populates='devices')

    data = db.relationship('Data', backref='device', lazy=True)

    def create_device(name, device_type, unit, is_active, kit_id):
        device = Device(name=name, device_type=device_type, unit = unit, is_active=is_active, kit_id=kit_id)
        db.session.add(device)
        db.session.commit()
        return device
    
    def get_device_by_id(id):
        return Device.query.filter_by(id = id).first()
    
    def get_device_by_name(name):
        return Device.query.filter_by(name = name).first()

    def get_devices_by_type(device_type):
        return Device.query.filter_by(device_type=device_type).all()

    def get_all_devices():
        return Device.query.all()

    def delete_device(device_id):
        device = Device.query.get(device_id)
        if device:
            db.session.delete(device)
            db.session.commit()

    def edit_device(id, name, device_type, unit, is_active, kit_id):
        device = Device.query.filter(Device.id == id).first()
        if device is not None:
            device.name = name
            device.device_type = device_type
            device.unit = unit
            device.is_active = is_active
            device.kit_id = kit_id
            db.session.commit()

            return Device.get_all_devices()