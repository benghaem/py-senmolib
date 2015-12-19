import argparse 
import zmq
from .base import Base

class Fusion(Base):

	def __init__(self, buffer_size, no_dupl):
		super(Fusion, self).__init__()
		self.buffer = []
		self.no_dupl = no_dupl
		self.buffer_size = buffer_size

	def start(self):
		while self.running:
			data = self.decode(self.receiver.recv()))
			fusion_data = self.push_to_buffer(data)
			if fusion_data != None:
				sender.send(self.encode(fusion_data))

	def push_to_buffer(self, data):
		print("pushing to puffer",data)
		result = None
		if not self.no_dupl:
			self.buffer += data
		else:
			for val in data:
				if val not in self.buffer:
					self.buffer.append(val)

		if len(self.buffer) >= self.buffer_size:
			result = self.fuse(self.buffer[0:buffer_size])
			self.buffer = self.buffer[:buffer_size]
		return result

	def fuse(self, data):
		return data