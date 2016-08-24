#!/usr/bin/env python

import sys
import time

try:
    import serial
except ImportError:
    exit("This library requires the serial module\nInstall with: sudo pip install pyserial")

import p1.loader


print('Setting up Propeller HAT')
l = p1.loader.Loader('/dev/ttyAMA0',17)
l.upload(path='SIDcogSlave.binary',progress=p1.loader.print_status)
time.sleep(0.1)

# Comment the line below to enable the (slow) Python sid player
exit('Now use ./sidplay tunes/<filename> to play a tune!')

play_rate = 50 #Hz

if len(sys.argv) < 2:
  exit("Usage: " + sys.argv[0] + " <dump>")

s = serial.Serial('/dev/ttyAMA0',115200)

f = open(sys.argv[1],'rb')

d = f.read()

f.close()

reg_size = 25


def chunks(l, n):
  for i in range(0, len(l), n):
    yield l[i:i+n]

chunks = list(map(lambda x: chr(13) + 'SDMP' + ''.join(x), chunks(d, reg_size)))

for chunk in chunks:
  print(list(ord(x) for x in chunk))
  s.write(chunk)
  s.flush()
  time.sleep(1.0/play_rate)

