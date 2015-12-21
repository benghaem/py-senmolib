import zmq

class Monitor(object):
	"""Allows the creation of simple monitors that allow"""
	def __init__(self, arg):
		super(Monitor, self).__init__()
		self.arg = arg
		          