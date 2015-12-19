import zmq
import argparse
import msgpack

class Base(object):

	def __init__(self, bind_send=False, verbose=False):
		super(Base, self).__init__()
		self.context = zmq.Context()
		parser = argparse.ArgumentParser()
		parser.add_argument('input_port')
		parser.add_argument('output_port')
		parser.add_argument('identity')

		args = parser.parse_args()

		self.running = True
		self.verbose = verbose
		# Socket to receive messages on
		self.receiver = self.context.socket(zmq.PULL)
		self.receiver.connect("tcp://localhost:"+str(args.input_port))

		# Socket to send messages to
		self.sender = self.context.socket(zmq.PUSH)
		if bind_send:
			self.sender.bind("tcp://*:"+str(args.output_port))
		else:
			self.sender.connect("tcp://localhost:"+str(args.output_port))

	def start(self):
		raise NotImplementedError

	def decode(self, data_in):
		data = msgpack.unpackb(data_in, use_list=False)
		return datas

	def encode(self, data_out):
		return msgpack.packb(data)
	