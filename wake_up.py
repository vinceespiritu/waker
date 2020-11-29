import paho.mqtt.client as mqtt
import pygame
import time

audio_filename = "wakemeup.mp3"



# Wakeup function
def status_callback(client, userdata, message):

	pygame.mixer.init()
	pygame.mixer.music.load("wakemeup.mp3")
	if(message.payload == "SLEEP_ON"):
		#play music
	
		pygame.mixer.music.play()

	elif(message.payload == "SLEEP_OFF"):
		#stop music afer 10 seconds
		pygame.mixer.music.pause()

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("waker/sleep_status")
    client.message_callback_add("waker/sleep_status", status_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while 1:
    	time.sleep(0.10)