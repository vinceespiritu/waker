## Driver Waker
## Inspiration
To keep the road safer for all drivers at night. According to the National Highway Traffic Safety Administration, there are about 100,000 police-reported crashes annually caused by drowsy driving.

## What it does
Driver Waker automatically plays lively music whenever it detects the driver falling asleep. It keeps the driver awake at all times by waking them up from the loud music.

## How we built it
We use OpenCV for eye detection. Once the program detects the driver's eyes are closed for around 2 seconds, the program in the Virtual Machine will send a message to the MQTT broker that represents the sleep status of the driver. On the other node, the RaspberrypPi will receive the message and play the music if the sleep status is on, which means that driver is falling asleep. Otherwise, it will stop the music once the driver is awake.

## Challenges we ran into
+ Bug fixes on the algorithm for eye detection
+ pygame python package incompatibility
+ Bluetooth speaker connection on raspberry pi

## Accomplishments that we're proud of
+ Successfully creating the algorithm for eye detection
+ Completing the project on time

## What we learned
+ pygame python library capability
+ OpenCV capability

## What's next for Driver Waker
+ Add an extra LED Indicator on the vehicle to alert other cars when the driver is falling asleep
+ Add a webpage or create a log file to record all the times when the driver was about to fall asleep while driving.
+ Based on the data pattern, our technology can inform the driver of the times he/she must be extra careful when driving or avoid driving.
 
