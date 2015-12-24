from .base import Base
import zmq
import msgpack
import time

class Vent(Base):
	"""
	A class that defines a senmo vent component. The ventilator sends windows of the input stream off to worker components.

	Args:
		window_size: An int, number of values from the data stream to buffer before sending to a worker
		window_offset: An int, the number of new values required before sending another window
	"""

	def __init__(self, window_size, window_offset, **kwargs):
		super(Vent, self).__init__(**kwargs)
		self.buffer = []
		self.buffer_max = window_size
		self.window_offset = window_offset

		# Socket to receive messages on
		self.receiver = self.context.socket(zmq.PULL)
		self.receiver.connect("tcp://localhost:"+str(self.source_port))

		# Socket to send messages to
		self.sender = self.context.socket(zmq.PUSH)
		self.sender.bind("tcp://*:"+str(self.worker_port))

		# Socket to trigger fusion with
		self.fusion = self.context.socket(zmq.PUSH)
		self.fusion.connect("tcp://localhost:"+str(self.fusion_port))

	def start(self):
		"""
		Start the ventilator

		Sends a message to the fusion component to ensure that it is active before buffering input and sending complete windows to the workers
		"""
		waiting = True
		while waiting:
			try:
				self.fusion.send(msgpack.packb("a tasty snack"), zmq.NOBLOCK)
				waiting = False
			except zmq.ZMQError as e:
				time.sleep(1)

		while self.running: 
			data = self.decode(self.receiver.recv())
			windows = self.update_buffer(data)
			if windows != None:
				for window in windows:
					self.sender.send(self.encode(window))
	
	def update_buffer(self, data):
		"""
		Pushes data to the buffer

		Args:
			data: a python object to add to the buffer

		Returns:
			list: a list of python objects of length 'window_size'

		"""
		windows = []
		self.buffer.append(data)

		while len(self.buffer) >= self.buffer_max:
			windows.append(self.buffer[0:self.buffer_max])
			self.buffer = self.buffer[self.window_offset:]

		return windows
