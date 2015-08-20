#! /bin/python

import argparse
import zmq
import numpy as np
import time

np.set_printoptions(threshold=np.nan)
context = zmq.Context()

parser = argparse.ArgumentParser()
parser.add_argument('input_port')
parser.add_argument('fusion_port')
parser.add_argument('identity')

args = parser.parse_args()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:"+args.input_port)

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:"+args.fusion_port)

while True:
	data_arry = receiver.recv_pyobj()
	# print("Got job!")

	x_vals = [set[0] for set in data_arry]
	y_vals = [set[1] for set in data_arry]

	# print("x vals:" + str(x_vals))
	# print("y vals:" + str(y_vals))

	#threshold
	th = 1.5*np.std(y_vals)

	# print("threshold:"+str(th))

	data_der = np.ediff1d(y_vals)

	x_loc = []

	for i in range(1, len(y_vals)-1):
		if data_der[i-1] > 0 and data_der[i] <= 0 and y_vals[i] >= th:
			x_loc.append(x_vals[i])

	sender.send_pyobj(x_loc)
	# print("Finished job!")
	# print(time.time())

