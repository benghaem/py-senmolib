from senmolib.components.worker import Worker

class myWorker(Worker):
	def process(self, arr):
		print(self.identity,arr)
		total = 0
		for el in arr:
			try:
				val = int(el)
			except:
				val = 0
			total += val
		return [total]

myWorker().start()