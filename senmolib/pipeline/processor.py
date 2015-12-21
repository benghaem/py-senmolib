import subprocess
import zmq as zmq
import time

class Processor(object):
	"""Processor launches real processes and configures data flow between processing and fusion components.

	Processor is useful when one would like to use a mix of senmo components that may be implemented across languages. If one is using components that are only written in Python, PureProcessor may be preferable as all components may be defined within the same file. 

	Args:
		port_list: A length 4 list of port values. For example, [5000,5001,5002,5003]. The first value is the input port, the second the worker port, the third the fusion port, and the fourth the output port. 
		process_count: An int. The number of worker processes to start
		vent_path:   A string. an absolute path to the vent component
		worker_path: A string. an absolute path to the worker component
		fusion_path: A string. an absolute path to the fusion component
		identifier: A string to identify the processor
	"""
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
		"""Start processes
		
		Starts the defined number of worker processes as well as the fusion and vent components

		"""
		# start workers
		self.add_worker_process(self.process_count)

		# Fusion launch
		self.fusion_controller = Process(self.identifier+"-fusion", self.fusion_path, self.port_list)
		
		# Vent launch
		self.vent_controller = Process(self.identifier+"-vent", self.vent_path, self.port_list)

		self.running = True

	def add_worker_process(self, num):
		"""Starts a additional set of worker processes

		Args: 
			num: an int. The number of additional  worker processes to start

		"""

		for i in range(num):
				new_process = Process(self.identifier+"-p-"+str(i+self.iid_offset), self.process_path, self.port_list)
				self.process_controlers.append(new_process)
		
		self.iid_offset += num


	def stop(self):
		"""Stop all worker processes as well as the fusion and vent components"""
		for pc in self.process_controlers:
			pc.stop()
		self.fusion_controller.stop()
		self.vent_controller.stop()
		
		#Reset controllers
		self._reset_controllers()

	def reload_processes(self, kill=False, rolling=False):
		"""Reloads all worker processes. By default will stop and then restart all processes. Enabling rolling will keep the workers running while reloading worker processes sequentially.

		Args:
			kill: A boolean. If True, kill proesses instead of stopping them
			rolling: A boolean. If True, reload processes sequentially
		"""
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
		"""Kill all worker processes as well as fusion and vent components"""
		for pc in self.process_controlers:
			pc.kill()
		self.fusion_controller.kill()

		self._reset_controllers()

	def restart(self):
		"""Stop and then restart all worker processes and fusion/vent components"""
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

		Returns:
			list: A list of all pids, where the fusion component is first, the vent component is second, and the worker processes follow
		"""
		return [self.fusion_controller.get_pid()] + [self.vent_controller.get_pid()] + [pc.get_pid() for pc in self.process_controlers]

	def process_count(self):
		"""
		Returns number of active worker processes

		Returns:
			int: number of active worker processes
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