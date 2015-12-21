
Components
====================================

A selection of component classes that can be extended to create senmo compatible programs.

For example, a simple ventilator::

	#! /bin/python

	import senmolib

	myVent = senmolib.components.Vent(50,25)

	myVent.start()

which you can run like this (assuming the file was named myVent.py)::
	
	./myVent.py input_port worker_port fusion_port output_port identifier

More examples are available in the examples folder of the repo

.. automodule:: senmolib.components
.. currentmodule:: senmolib.components


:class:`Base`
-------------

.. autoclass:: Base
   :members:


:class:`Vent`
-------------

.. autoclass:: Vent
   :members:

:class:`Worker`
---------------

.. autoclass:: Worker
   :members:

:class:`Fusion`
---------------

.. autoclass:: Fusion
   :members: