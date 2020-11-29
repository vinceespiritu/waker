import paho.mqtt.client as mqtt
import pygame
import time

audio_filename = "wakemeup.mp3"
pygame.mixer.init()
pygame.mixer.music.load("wakemeup.mp3")


# Wakeup function
def status_callback(client, userdata, message):

	
	
	if(message.payload == "SLEEP_ON"):
		#play music
		pygame.mixer.music.play(start = 36.0)

	elif(message.payload == "SLEEP_OFF"):
		#stop music afer 10 seconds
		pygame.mixer.music.stop()

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("waker/sleep_status")
    client.message_callback_add("waker/sleep_status", status_callback)

def on_disconnect(client, userdata, rc):
    print("Disconnected from server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while 1:
    	time.sleep(0.10)