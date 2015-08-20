import zmq

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

while True:
	data = receiver.recv_pyobj()

	data_x_sum = 0
	for item in data:
		data_x_sum = data_x_sum + item[0]

	print(len(data),"Avg: "+str(data_x_sum / len(data)))