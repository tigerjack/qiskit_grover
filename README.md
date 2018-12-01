# qiskit_grover
An implementation of Grover's algorithm on qiskit using up to 3 qubits.
In other words, it can correctly search for a specific entry in a database of up to 2^3 entries.

## Prerequisites ##
It requires the [qiskit development kit](https://github.com/Qiskit/qiskit-terra). Take a look at the repo for a full reference, or just install it using

```
pip install qiskit
```

Note that, in order to run a simulation on a real device, you also need to get an account from ibmq. The qiskit repository contains all the necessary info.

## Usage ##
Check the `grover_test.py` file and in particular the `usage()` function to get an idea on how it works.

### As a module ###
Import the `grover_test` module in a python interpreter and run the `build_and_run(n, x_star, real, backend_name)` function. 
  * `n` is the number of qubits (2 or 3)
  * `x_star` is the marked state (between 0 and 2**n), i.e. the (only) state for which the oracle function returns 1. In general, the oracle should be a black box emitting 1 only on a specific input state. Obviously, in our case, we have to build the oracle ourself.
  * `real` is True for a real backend, False (default) for the qasm simulator.
  * `backend_name` is the name of the backend you want to use; omit it if you want a default choice. Most of the time, you want to leave it blank.
  
For example, if you want to run an experiment on a real device with 3 qubits and selecting 5 as the x_star of the oracle, just run

``` python
import grover_test as gt

gt.build_and_run(3, 5, True, None)
```
  
or to run a simulation with 2 qubits and 3 as the special x_star state

``` python
import grover_test as gt

gt.build_and_run(2, 3, True, None)
```

### From command line ###
You can also run the `grover_test.py` file from the command line. It can take up to 5 arguments:
  * `n` (default 2)
  * `x_star` (default 3)
  * `real` (default False)
  * `infos` the only parameter different from the previous case; you can set it to 1 to only get some useful infos on the compiled circuit built for the specific backend. This is useful to see how many gates a backend uses to implement the circuit. At the time of writing, ibmqx2 and ibmqx4 take ~60 gates, while ibmqx5 and ibmq_16_melbourne take ~200 gates.
  * `backend_name`

For the same examples as for the case above, we could write
``` bash
>python src/grover_test.py 3 5 1
>python src/grover_test.py 2 3 0
```

If instead we only want to know how many gates are needed for the ibmq_16_melbourne device to run our first circuit

``` bash
>python src/grover_test.py 3 5 1 1 ibmq_16_melbourne
```

## Results ##
The results are promising even for real ibmq devices. However, due to the high number of gates used in ibmqx5 and ibmq_16_melbourne, those quantum devices return wrong results; ibmqx2 and ibmqx4, on the other hand, give the right answer with an high degree of accuracy.
