from .base import Base

class Worker(Base):
	def __init__(self, verbose=False):
		super(Worker, self).__init__(bind_send=False)

	def start(self):
		while self.running: 
			data = self.decode(self.receiver.recv())
			output = self.process(data)
			self.sender.send(self.encode(output))

	def process(self, arr):
		return arr

