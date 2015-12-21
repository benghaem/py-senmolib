#! /home/ben/programming/senmo/env/bin/python


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


file_loop = []

print("Bound to 5000")

with open('ecg_old.csv', 'r') as f:
	#get rid of garbage at top of file
	_ = f.readline()
	_ = f.readline()

	count = 0
	for line in f:

		time, y_val = line.split(',')


		full_tuple = (count,float(y_val))

		file_loop.append(float(y_val))

		socket.send(msgpack.packb(full_tuple))
		sleep(0.01)
		count = count + 1

	while True:
		for val in file_loop:
			socket.send(msgpack.packb((count,val)))
			sleep(0.01)
			count = count + 1
