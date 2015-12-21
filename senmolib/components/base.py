import zmq
import argparse
import msgpack

class Base(object):
	"""Class to provide common CLI argument requrirements and provide basic implimentation of encode and decode using msgpack

	Args:
		verbose: A boolean. If true the component may print debug info to the console

	"""

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
		"""Start the component. Must be implimented by subclass"""
		raise NotImplementedError

	def decode(self, data_in, allow_stop=True):
		"""
		Decode byte input using msgpack

		Args:
			data_in: bytes object from socket
			allow_stop: a boolean value that if set to true will allow the component to be stopped by passing ['senmo-stop']

		Returns:
			An object or None

		"""
		data = msgpack.unpackb(data_in, use_list=False)
		# Check for stop condition and return none if stopped
		if data == ['senmo-stop'] and allow_stop:
			self.running = False
			return None
		return data


	def encode(self, data):
		"""
		Encode object input using msgpack

		Args:
			data: an object to encode with msgpack

		Returns:
			A bytes object
		"""
		return msgpack.packb(data)
	