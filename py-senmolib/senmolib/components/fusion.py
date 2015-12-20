from .base import Base
import zmq

class Fusion(Base):

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
		# eat start message from vent
		print("waiting for snack from the vent on", self.fusion_port)
		self.receiver.recv()
		print("ate the snack from the vent")
		while self.running:
			data = self.decode(self.receiver.recv())
			fusion_data = self.push_to_buffer(data)
			if fusion_data != None:
				self.sender.send(self.encode(fusion_data))

	def push_to_buffer(self, data):
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
		return data