#! /bin/python


# Python server implimentation
# Binds a PUB socket to 5000
# Sends fake sensor data
#

import zmq
import msgpack
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5000")

print("Bound to 5000")

with open('ecg_old.csv', 'r') as f:
	#get rid of garbage at top of file
	_ = f.readline()
	_ = f.readline()

	count = 0
	while True:

		time, y_val = f.readline().split(',')

		full_tuple = (count,float(y_val))

		socket.send(msgpack.packb(full_tuple))
		sleep(0.01)
		count = count + 1
