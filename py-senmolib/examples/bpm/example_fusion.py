#! /bin/python

from senmolib.components.fusion import Fusion
import numpy as np

class exampleFusion(Fusion):
	def fuse(self, arr):
		print(len(arr))
		hr_sp = np.ediff1d(arr)
		bpm_mv_avg = 100/np.average(hr_sp) * 60

		return bpm_mv_avg

exampleFusion(10,True).start()