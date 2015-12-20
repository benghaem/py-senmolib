import zmq
import argparse
import msgpack

class Base(object):

	def __init__(self, verbose=False):
		super(Base, self).__init__()
		self.context = zmq.Context()
		parser = argparse.ArgumentParser()
		parser.add_argument('source_port')
		parser.add_argument('worker_port')
		parser.add_argument('fusion_port')
		parser.add_argument('output_port')
		parser.add_argument('identity')

		args = parser.parse_args()

		self.running = True
		self.verbose = verbose
		self.identity = args.identity
		self.source_port = args.source_port
		self.worker_port = args.worker_port
		self.fusion_port = args.fusion_port
		self.output_port = args.output_port

	def start(self):
		raise NotImplementedError

	def decode(self, data_in):
		data = msgpack.unpackb(data_in, use_list=False)
		if data != ['senmo-stop']:
			return data
		else:
			self.running = False
			return None

	def encode(self, data):
		return msgpack.packb(data)
	