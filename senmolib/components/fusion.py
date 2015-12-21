from .base import Base
import zmq

class Fusion(Base):
	"""A class that may be subclassed to implement a senmo fusion component. By default this component will wait for its buffer to fill before running the fuse() method

	Args:
		buffer_size: An int indicating the size of the internal buffer
		no_dupl: A boolean indicating if the buffer should ignore duplicates

	Note:
		fuse() should be redefined by all subclasses as the reference implementation does nothing

	"""

	def __init__(self, buffer_size, no_dupl):
		super(Fusion, self).__init__()
		self.buffer = []
		self.no_dupl = no_dupl
		self.buffer_size = buffer_size

		# Socket to receive messages on
		self.receiver = self.context.socket(zmq.PULL)
		self.receiver.bind("tcp://*:"+str(self.fusion_port))

		# Socket to send messages to
		self.sender = self.context.socket(zmq.PUSH)
		self.sender.bind("tcp://*:"+str(self.output_port))

	def start(self):
		"""
		Start the component.

		Decodes data from the receiver socket and then calls push_to_buffer. If push_to_buffer returns data, the data is then encoded and sent.
		"""

		# eat start message from vent
		self.receiver.recv()
		while self.running:
			data = self.decode(self.receiver.recv())
			fusion_data = self.push_to_buffer(data)
			if fusion_data != None:
				self.sender.send(self.encode(fusion_data))

	def push_to_buffer(self, data):
		"""
		Pushes data into internal buffer and runs fuse() if the buffer is full.

		Args:
			data: a list of items to add to the buffer

		Returns:
			object: the result of fuse() on the buffer if the buffer was full
		"""
		result = None
		if not self.no_dupl:
			self.buffer += data
		else:
			for val in data:
				if val not in self.buffer:
					self.buffer.append(val)

		if len(self.buffer) >= self.buffer_size:
			result = self.fuse(self.buffer[0:self.buffer_size])
			self.buffer = self.buffer[-self.buffer_size:]

		return result

	def fuse(self, data):
		"""
		Fuses an list of data. #The reference implementation of this function does nothing# and thus it should be redefined when subclassed

		Args:
			data: A list of data from the internal buffer

		Returns:
			object: Data in some format to be serialized by msgpack

		"""
		return data