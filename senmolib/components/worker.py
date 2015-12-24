from .base import Base
import zmq

class Worker(Base):
	"""
	A class that may be subclassed to implement senmo worker components. 

	Note:
		process() should be redefined by all subclasses as the reference implementation does nothing.
	"""
	def __init__(self, **kwargs):
		super(Worker, self).__init__(**kwargs)
		# Socket to receive messages on
		self.receiver = self.context.socket(zmq.PULL)
		self.receiver.connect("tcp://localhost:"+str(self.worker_port))

		# Socket to send messages to
		self.sender = self.context.socket(zmq.PUSH)
		self.sender.connect("tcp://localhost:"+str(self.fusion_port))

	def start(self):
		"""
		Start the worker

		Receives objects from the ventilator and then passes them to the process method
		"""
		while self.running:
			data = self.decode(self.receiver.recv())
			output = self.process(data)
			self.sender.send(self.encode(output))

	def process(self, data):
		"""
		Process the data object

		Args:
			data: a python object

		Returns:
			object: a python object to be sent to fusion
		
		"""
		return data

