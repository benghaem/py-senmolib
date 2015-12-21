#! /bin/bash

# on 5000 pub
python example_ecg_producer.py &
python example_vent.py 8000 8001 8002 8003 vent &

for i in 1 2 3 4 5
do
	python example_ecg_worker.py 8000 8001 8002 8003 $i &
done

python example_fusion.py 8000 8001 8002 8003 fusion &