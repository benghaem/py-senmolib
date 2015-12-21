#! /home/ben/programming/senmo/env/bin/python

from senmolib.components.worker import Worker
import numpy as np

class exampleEcgWorker(Worker):

	def process(self, data_arr):
		x_vals =[item[0] for item in data_arr]
		y_vals =[item[1] for item in data_arr]
		print(self.identity,"have x,y",x_vals[0],y_vals[0])

		#threshold
		th = 1

		data_der = np.ediff1d(y_vals)

		x_locs = []

		for i in range(1, len(y_vals)-1):
			if data_der[i-1] > 0 and data_der[i] <= 0 and y_vals[i] >= th:
				x_locs.append(x_vals[i])

		print(self.identity,"computed",x_locs)
		return x_locs

exampleEcgWorker().start()