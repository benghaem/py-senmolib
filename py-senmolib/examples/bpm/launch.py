import senmolib

base_path = "/home/ben/programming/senmo/process/py-senmolib/examples/bpm/"

processor = senmolib.pipeline.Processor([8000,8001,8002,8003],4,base_path+'example_vent.py',base_path+'example_ecg_worker.py',base_path+'example_fusion.py','bpm')

processor.start()

while True:
	cmd = input('>')
	if cmd == "list":
		print(processor.list_pids())
	elif cmd == "add":
		processor.add_worker_process(1)
	elif cmd == "stop":
		processor.stop()
		print("Stopping processor")
	elif cmd == "start":
		processor.start()
		print("Starting processor")
	elif cmd == "restart":
		processor.restart()
		print("Restarting processor")
	elif cmd == "exit":
		exit(0)

