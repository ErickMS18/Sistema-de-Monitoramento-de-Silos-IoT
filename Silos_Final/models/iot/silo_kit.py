from models.db import db
from models.iot.devices import Device

class Kit(db.Model):
    __tablename__ = 'kits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    devices = db.relationship('Device', back_populates='kit', lazy=True)

    @staticmethod
    def create_kit(name):
        kit = Kit(name=name)
        db.session.add(kit)
        db.session.commit()
        return kit

    @staticmethod
    def get_all_kits():
        return Kit.query.all()

    @staticmethod
    def delete_kit(kit_id):
        kit = Kit.query.get(kit_id)
        if kit:
            db.session.delete(kit)
            db.session.commit()
