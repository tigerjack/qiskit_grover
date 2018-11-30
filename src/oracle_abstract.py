class Oracle:
    """
    An abstract oracle for the Grover algorithm.
    """

    def __init__(self, n, x_star):
        """
        :param n: the number of input/output qubits of the oracle
        :param x_star: the value for which the oracle should return 1. It should be comprised b/w 0 and 2**n - 1
        """
        self.n = n
        self.x_star = x_star

    def get_circuit(self, qr, qc):
        """
        This abstrac method should be implemented by the real subclasses.
        This method doesn't return anything. It expects a quantum circuit qc and an array
        of quantum registers qr and it simply adds the appropriate gates to the circuit
        and registers.
        :param qr: the qiskit QuantumRegister array
        :param qc: the qiskit QuantumCircuit
        :returns: nothing, but the real subclasses that overwrite it should return the original QuantumCircuit qc with the addition of the appropriate gates for the Grover algorithm

        """
        raise NotImplementedError("Should have implemented this")
