from math import sqrt, pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def get_circuit(n, oracle):
    """
    Build the circuit composed by the oracle black box and the other quantum gates.
    :param n: The number of qubits
    :param oracle: The black box (quantum) oracle
    :returns: The proper quantum circuit
    :rtype: qiskit.QuantumCircuit
    """

    qr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)

    # Initial superposition
    qc.h(qr)

    # Grover's algorithm is a repetition of an oracle box and a diffusion box.
    # The number of repetitions is given by the following formula.
    r = int(round((pi / 2 * sqrt(2**n) - 1) / 2))
    print("Repetition of ORACLE+DIFFUSION boxes required: {0}".format(r))
    for j in range(r):
        oracle.get_circuit(qr, qc)
        diffusion(qr, qc)

    qc.measure(qr, cr)
    return qc


def diffusion(qr, qc):
    """
    The Grover diffusion operator.
    Given the arry of qiskit QuantumRegister qr and the qiskit QuantumCircuit qc, it adds the diffusion operator to the appropriate qubits in the circuit.
    """
    n = len(qr)
    qc.h(qr)

    # D matrix, flips state |000> only (instead of flipping all the others)
    qc.x(qr)
    n_controlled_Z_circuit(qc, [qr[j] for j in range(n - 1)], qr[n - 1])
    qc.x(qr)

    qc.h(qr)


def n_controlled_Z_circuit(qc, controls, target):
    """
    Build a CZ circuit w/ a variable number of control qubits and just one target.
    At the moment, it only works with 1 or 2 control bits and uses for them CX and CCX gates respectively.
    """
    if (len(controls) > 2):
        raise ValueError(
            "At the moment, the CZ should have at most 2 control qubits")
    qc.h(target)
    if (len(controls) == 1):
        qc.cx(controls[0], target)
    else:  # len == 2
        qc.ccx(controls[0], controls[1], target)
    qc.h(target)
