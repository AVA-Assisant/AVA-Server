from app import app, db, mqttc, socketio_app, Devices
from flask_socketio import emit
import json


@socketio_app.on('setup')
def setup(devices):
    for device in devices:
        db_record = Devices.query.filter_by(
            _mqttId=device["mqtt_Id"]).first()
        if (db_record):
            device["status"] = db_record._status
            device["settings"] = db_record._settings
        else:
            newDevice = Devices(
                _id=int(device["id"]), _type=device["type"], _mqttId=device["mqtt_Id"], _status="Off")
            db.session.add(newDevice)
            db.session.commit()

    emit("setup", devices)


@socketio_app.on('changeState')
def setup(device):
    dbDev = Devices.query.filter_by(
        _mqttId=device["mqtt_Id"]).first()
    dbDev._settings = device['settings']
    dbDev._status = device['status']
    db.session.commit()
    mqttc.publish(device["mqtt_Id"], json.dumps(
        device['settings']))
    if device['emit']:
        emit("stateChanged", device, broadcast=True)
