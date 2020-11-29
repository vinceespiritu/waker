import paho.mqtt.client as mqtt
from pynput import keyboard
import time


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_disconnect(client, userdata, rc):
    print("Disconnected from server (i.e., broker) with result code "+str(rc))

def on_press(key):
	try:
		k = key.char
	except:
		k = key.name

	if k == "a":
		client.publish("waker/sleep_status","SLEEP_ON")
		print("SLEEPING")
	
	elif k == "i":
		client.publish("waker/sleep_status","SLEEP_OFF")
		print("AWAKE")

	elif k =="q":
		client.disconnect()
		print("Disconnecting...")

if __name__ == '__main__':

	lis = keyboard.Listener(on_press=on_press)
	lis.start()

	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect
	client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
	client.loop_start()

	while 1:
		time.sleep(0.10)
    	