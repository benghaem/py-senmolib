import subprocess
import zmq as zmq
import time

class Processor(object):
	"""Processor launches processes and configures data flow between processing and fusion components"""
	def __init__(self, port_list, process_count, vent_path, worker_path, fusion_path, identifier):
		super(Processor, self).__init__()

		#State
		self.running = False
		
		#Process settings
		self.process_count = int(process_count)
		self.identifier = identifier
		self.process_path = worker_path
		self.fusion_path = fusion_path
		self.vent_path = vent_path
		self.port_list = [str(val) for val in port_list]
		
		#Controller Listing
		self.process_controlers = []
		self.fusion_controller = None
		self.vent_controller = None
		self.iid_offset = 0
		
		#ZMQ context and socket

	def start(self):
		"""Start processes"""
		# start workers
		self.add_worker_process(self.process_count)

		# Fusion launch
		self.fusion_controller = Process(self.identifier+"-fusion", self.fusion_path, self.port_list)
		
		# Vent launch
		self.vent_controller = Process(self.identifier+"-vent", self.vent_path, self.port_list)

		self.running = True

	def add_worker_process(self, num):
		for i in range(num):
				new_process = Process(self.identifier+"-p-"+str(i+self.iid_offset), self.process_path, self.port_list)
				self.process_controlers.append(new_process)
		
		self.iid_offset += num


	def stop(self):
		"""Stop processes and fusion"""
		for pc in self.process_controlers:
			pc.stop()
		self.fusion_controller.stop()
		self.vent_controller.stop()
		
		#Reset controllers
		self._reset_controllers()

	def reload_processes(self, kill=False, rolling=False):
		"""Reloads all processes. By default will disable the processor and restart all processes. Enabling rolling will keep the processor running while reloading processes sequentially."""
		if rolling:
			for pc in self.process_controlers:
				pc.restart(kill=kill)
		else:
			self.running = False
			for pc in self.process_controlers:
				if kill:
					pc.kill()
				else:
					pc.stop()

			for pc in self.process_controlers:
				pc.start()
			self.running = True

	def reload_fusion(self, kill=False, hard_reload=True):
		"""Reloads the fusion process. Setting hard_reload to false will keep the processor running while the process is reloaded"""
		if hard_reload:
			self.running = False

		if kill:
			self.fusion_controller.kill()
		else:
			self.fusion_controller.stop()

		self.running = True

	def kill(self):
		"""Kill processes and fusion"""
		for pc in self.process_controlers:
			pc.kill()
		self.fusion_controller.kill()

		self._reset_controllers()

	def restart(self):
		self.stop()
		self.start()

	def _reset_controllers(self, vent=True, fusion=True, process=True, running=True):
		if fusion:
			self.fusion_controller = None
		if vent:
			self.vent_controller = None
		if process:
			self.process_controllers = []
		if running:
			self.running = False

	def list_pids(self):
		"""
		Returns a list of process pids	
		"""
		return [self.fusion_controller.get_pid()] + [self.vent_controller.get_pid()] + [pc.get_pid() for pc in self.process_controlers]

	def process_count(self):
		"""
		Returns number of active processes

		*Ignores fusion controller
		"""

		return len(self.process_controlers)
			
class Process(object):
	"""Wrapper for subprocess that allows restarting of processes"""
	def __init__(self, identifier, path, port_list, start=True):
		super(Process, self).__init__()
		self.path = path
		self.port_list = port_list
		self.identifier = identifier

		self.complete_args = [self.path] + self.port_list + [self.identifier]

		if start:
			self.start()

	def start(self):
		print(self.complete_args)
		self.process_instance = subprocess.Popen(self.complete_args)

	def stop(self):
		self.process_instance.terminate()

	def kill(self):
		self.process_instance.kill()

	def get_pid(self):
		return self.process_instance.pid

	def restart(self, kill=False):
		#Stop process
		if kill:
			self.kill()
		else:
			self.stop()
		#Restart
		self.start()