from .base import Base
import zmq
import msgpack
import time

class Vent(Base):
	def __init__(self, window_size, window_offset, verbose=False):
		super(Vent, self).__init__()
		self.buffer = []
		self.buffer_max = window_size
		self.window_offset = window_offset

		# Socket to receive messages on
		self.receiver = self.context.socket(zmq.PULL)
		print("going to recv messages on",self.source_port)
		self.receiver.connect("tcp://localhost:"+str(self.source_port))

		# Socket to send messages to
		print("going to send messages on",self.worker_port)
		self.sender = self.context.socket(zmq.PUSH)
		self.sender.bind("tcp://*:"+str(self.worker_port))

		# Socket to trigger fusion with
		print("going to trigger fusion messages on",self.fusion_port)
		self.fusion = self.context.socket(zmq.PUSH)
		self.fusion.connect("tcp://localhost:"+str(self.fusion_port))

	def start(self):
		print("about to send fusion a snack")
		waiting = True
		while waiting:
			try:
				self.fusion.send(msgpack.packb("a tasty snack"), zmq.NOBLOCK)
				waiting = False
			except zmq.ZMQError as e:
				print("fusion not ready trying again in 1 second", e)
				time.sleep(1)

		print("Sent fusion a snack")
		while self.running: 
			data = self.decode(self.receiver.recv())
			windows = self.update_buffer(data)
			if windows != None:
				for window in windows:
					self.sender.send(self.encode(window))
	
	def update_buffer(self, data):
		windows = []
		self.buffer.append(data)

		while len(self.buffer) >= self.buffer_max:
			windows.append(self.buffer[0:self.buffer_max])
			self.buffer = self.buffer[self.window_offset:]

		return windows
