from .base import Base

class Vent(Base):
	def __init__(self, window_size, window_offset, verbose=False):
		super(Vent, self).__init__(bind_send=True)
		self.buffer = []
		self.buffer_max = window_size
		self.window_offset = window_offset

	def start(self):
		while self.running: 
			data = self.decode(self.receiver.recv())
			windows = self.update_buffer(data)
			if windows != None:
				for window in windows:
					self.sender.send_string(self.encode(window))
	
	def update_buffer(self, data):
		windows = []
		self.buffer.append(data)

		while len(self.buffer) >= self.buffer_max:
			windows.append(self.buffer[0:self.buffer_max])
			self.buffer = self.buffer[self.window_offset:]

		return windows
		


