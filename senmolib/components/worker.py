from .base import Base
import zmq

class Worker(Base):
	def __init__(self, **kwargs):
		super(Worker, self).__init__(**kwargs)
		# Socket to receive messages on
		self.receiver = self.context.socket(zmq.PULL)
		self.receiver.connect("tcp://localhost:"+str(self.worker_port))

		# Socket to send messages to
		self.sender = self.context.socket(zmq.PUSH)
		self.sender.connect("tcp://localhost:"+str(self.fusion_port))

	def start(self):
		while self.running:
			data = self.decode(self.receiver.recv())
			output = self.process(data)
			self.sender.send(self.encode(output))

	def process(self, data):
		return data

