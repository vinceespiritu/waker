from pygame import mixer
import time

if __name__ == '__main__':
	mixer.init()
	mixer.music.load("wakemeup.mp3")
	mixer.music.play(start = 36.0)

	time.sleep(30)

	mixer.music.stop()