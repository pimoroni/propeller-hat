#!/usr/bin/env python

import subprocess
import time

try:
    import smbus
except ImportError:
    if sys.version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif sys.version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")

try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")

    
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT,initial=GPIO.HIGH)
GPIO.output(17,GPIO.LOW)
time.sleep(0.01)
GPIO.output(17,GPIO.HIGH)
time.sleep(1)

bus = smbus.SMBus(1)

#proc = subprocess.Popen(['p1load','-e','-r','SIDcogSlave.binary'])
#proc.wait()

duration = 120

# File, Time seconds, speed hz
playlist = [
    ('Eskimonika',220,250),
    ('Boten_Anna',100,duration),
    ('All_That_She_Wants_8580',120,duration),
    ('Scream',60,duration),
    ('Polyphonica',60,50),
    ('Alternative_Fuel',50,duration),
    ('Vibralux',50,duration),
    ('Super_Mario_Land',50,duration)
]

proc = None

while True:
  for song, speed, duration in playlist:
    print("Playing {} for {}".format(song, duration))
    proc = subprocess.Popen(['./sidplay','sid/{}.dmp'.format(song),str(speed),str(duration)])
    while proc.poll() is None:
      try:
        button = bus.read_byte_data(0x14,0x00)
        if button:
          proc.kill()
          while bus.read_byte_data(0x14,0x00):
            pass
          continue
      except IOError:
        pass
      time.sleep(0.01)
