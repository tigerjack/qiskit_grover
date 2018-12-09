from math import sqrt, pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import oracle_simple
import composed_gates


def get_circuit(n, oracles):
    """
    Build the circuit composed by the oracle black box and the other quantum gates.
    :param n: The number of qubits (not including the ancillas)
    :param oracles: A list of black box (quantum) oracles; each of them selects a specific state
    :returns: The proper quantum circuit
    :rtype: qiskit.QuantumCircuit
    """

    cr = ClassicalRegister(n)
    ## Testing
    if n > 3:
        #anc = QuantumRegister(n - 1, 'anc')
        # n qubits for the real number
        # n - 1 qubits for the ancillas
        qr = QuantumRegister(n + n - 1)
        qc = QuantumCircuit(qr, cr)
    else:
        # We don't need ancillas
        qr = QuantumRegister(n)
        qc = QuantumCircuit(qr, cr)
    ## /Testing
    print("Number of qubits is {0}".format(len(qr)))
    print(qr)

    # Initial superposition
    for j in range(n):
        qc.h(qr[j])

    # The length of the oracles list, or, in other words, how many roots of the function do we have
    m = len(oracles)
    # Grover's algorithm is a repetition of an oracle box and a diffusion box.
    # The number of repetitions is given by the following formula.
    print("n is ", n)
    r = int(round((pi / 2 * sqrt((2**n) / m) - 1) / 2))
    print("Repetition of ORACLE+DIFFUSION boxes required: {0}".format(r))
    oracle_t1 = oracle_simple.OracleSimple(n, 5)
    oracle_t2 = oracle_simple.OracleSimple(n, 0)
    for j in range(r):
        for i in range(len(oracles)):
            oracles[i].get_circuit(qr, qc)
            diffusion(n, qr, qc)

    for j in range(n):
        qc.measure(qr[j], cr[j])
    return qc, len(qr)


def diffusion(n, qr, qc):
    """
    The Grover diffusion operator.
    Given the arry of qiskit QuantumRegister qr and the qiskit QuantumCircuit qc, it adds the diffusion operator to the appropriate qubits in the circuit.
    """
    for j in range(n):
        qc.h(qr[j])

    # D matrix, flips state |000> only (instead of flipping all the others)
    for j in range(n):
        qc.x(qr[j])
    # 0..n-2 control bits, n-1 target, n..
    if n > 3:
        composed_gates.n_controlled_Z_circuit(
            qc, [qr[j] for j in range(n - 1)], qr[n - 1],
            [qr[j] for j in range(n, n + n - 1)])
    else:
        composed_gates.n_controlled_Z_circuit(
            qc, [qr[j] for j in range(n - 1)], qr[n - 1], None)

    for j in range(n):
        qc.x(qr[j])
    for j in range(n):
        qc.h(qr[j])
