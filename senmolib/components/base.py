import zmq
import argparse
import msgpack

class Base(object):
	"""Class to provide common CLI argument requrirements and provide basic implimentation of encode and decode using msgpack

	Args:
		pure: A boolean. If true use the values of identity and port_list instead of using an argument parser
		identity: A string: Used for identity if pure is True
		port_list: A list: Used to define ports if pure is True
		verbose: A boolean. If true the component may print debug info to the console

	"""

	def __init__(self, pure=False, identity="base", port_list=[], verbose=False):
		super(Base, self).__init__()
		self.context = zmq.Context()
		self.running = True
		self.verbose = verbose

		if pure == False:
			parser = argparse.ArgumentParser()
			parser.add_argument('source_port')
			parser.add_argument('worker_port')
			parser.add_argument('fusion_port')
			parser.add_argument('output_port')
			parser.add_argument('identity')

			args = parser.parse_args()

			self.identity = args.identity
			self.source_port = args.source_port
			self.worker_port = args.worker_port
			self.fusion_port = args.fusion_port
			self.output_port = args.output_port
		else:
			self.identity = identity
			self.source_port = port_list[0]
			self.worker_port = port_list[1]
			self.fusion_port = port_list[2]
			self.output_port = port_list[3]

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
	