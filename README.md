# qiskit_grover
An implementation of Grover's algorithm on qiskit.

## Prerequisites ##
It requires the [qiskit development kit](https://github.com/Qiskit/qiskit-terra). Take a look at the repo for a full reference, or just install it using

```
pip install qiskit
```

Note that, in order to run a simulation on a real device, you also need to get an account from ibmq. The qiskit repository contains all the necessary info.

## Usage ##
Check the `grover_test.py` file. Run `python grover_test.py -h` to get an idea on how it works.

### As a module ###
Import the `grover_test` module in a python interpreter and run the `build_and_run(n, x_star, real, backend_name)` function. 
  * `n` is the number of qubits (2 or 3)
  * `x_star` is the marked state (between 0 and 2**n), i.e. the (only) state for which the oracle function returns 1. In general, the oracle should be a black box emitting 1 only on a specific input state. Obviously, in our case, we have to build the oracle ourself.
  * `online` is True for an online IBMQ device, False (default) otherwise.
  * `real` is True for a real backend, False (default) for the qasm simulator. If it is set to True, the online option is automatically set to True also.
  * `backend_name` is the name of the backend you want to use; omit it if you want a default choice. Most of the time, you want to leave it blank. It makes sense only for an online experiment, because the only local backend is qasm.
  
For example, if you want to run an experiment on a real device with 3 qubits and selecting 5 as the x_star of the oracle, just run

``` python
import grover_test as gt

gt.build_and_run(3, 5, real=True, online=True)
```
Note that we can also omit the online parameter, which is automatically True when a real device is used.
  
or to run a local simulation with 2 qubits and 3 as the special x_star state 

``` python
import grover_test as gt

gt.build_and_run(2, 3, real=True)
```

### From command line ###
You can also run the `grover_test.py` file from the command line. You can see the full help by running `grover_test.py` with the `-h` flag.
Here is a brief description
```
usage: grover_test.py [-h] [-r] [-o] [-i] [-b BACKEND_NAME]
                      [--img_dir IMG_DIR] [--plot]
                      n x_star [x_star ...]
```

For the same examples as for the case above, we could write
``` bash
>python src/grover_test.py 3 5 -r
>python src/grover_test.py 2 3
```

If instead we only want to know how many gates are needed for the ibmq_16_melbourne device to run our first circuit

``` bash
>python src/grover_test.py 3 5 -r -i -b ibmq_16_melbourne
```

## Results ##
The results are promising even for real ibmq devices when n is less than 3. However, even in this case, due to the high number of gates used when compiling on ibmqx5 and ibmq_16_melbourne, those quantum devices return wrong results; ibmqx2 and ibmqx4, on the other hand, give the right answer with an high degree of accuracy.
For n > 3, the number of gates used is really huge and none of the device can really give a precise answer. The simulation, instead, always return the correct results.
