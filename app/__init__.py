from flask import Flask
import paho.mqtt.client as mqtt
from flask_sqlalchemy import SQLAlchemy


def on_connect(mqttc, obj, flags, rc):
    print("Connected!")


mqttc = mqtt.Client("Publisher")
mqttc.on_connect = on_connect
mqttc.connect("192.168.1.191", 2000)
mqttc.loop_start()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IoT_Devices.db'
db = SQLAlchemy(app)


class IoT_device(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
