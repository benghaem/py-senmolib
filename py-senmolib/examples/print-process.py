#! /bin/python

import zmq
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('input_port')
parser.add_argument('fusion_port')
parser.add_argument('identity')

context = zmq.Context()

args = parser.parse_args()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:"+args.input_port)

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:"+args.fusion_port)

while True:
	data_arr = receiver.recv_pyobj()
	print(time.time())
