import composed_gates


def negating_basis_state(n, qc, qr, x):
    """
    Negating basis state x out of n qubits (i.e. 2**n states). It adds the appropriate gates to negate the given x to the original QuantumCircuit qc.

    :param qc: the qiskit QuantumCircuit
    :param qr: the qiskit QuantumRegister, composed of n qubits
    :param x: the number to be negated, in the range 0..2**n-1
    """
    if (n == 2):
        if (x == 0):
            negating_00(qc, qr)
        elif (x == 1):
            negating_01(qc, qr)
        elif (x == 2):
            negating_10(qc, qr)
        elif (x == 3):
            negating_11(qc, qr)
        else:
            raise ValueError(
                "Oracle: Invalid value x_star {0} for n = {1}".format(x, n))
    elif (n == 3):
        if (x == 0):
            negating_000(qc, qr)
        elif (x == 1):
            negating_001(qc, qr)
        elif (x == 2):
            negating_010(qc, qr)
        elif (x == 3):
            negating_011(qc, qr)
        elif (x == 4):
            negating_100(qc, qr)
        elif (x == 5):
            negating_101(qc, qr)
        elif (x == 6):
            negating_110(qc, qr)
        elif (x == 7):
            negating_111(qc, qr)
        else:
            raise ValueError(
                "Oracle: Invalid value x_star {0} for n = {1}".format(x, n))
    elif n == 4:
        if (x == 15):
            negating_1111(n, qc, qr)
        else:
            raise ValueError(
                "Oracle: Invalid value x_star {0} for n = {1}".format(x, n))
    elif n == 5:
        if (x == 31):
            negating_11111(n, qc, qr)
        else:
            raise ValueError(
                "Oracle: Invalid value x_star {0} for n = {1}".format(x, n))
    else:
        raise ValueError("At the moment, the oracle works with up to 3 qubits")


def negating_11111(n, qc, qr):
    qc.h(qr[n - 1])
    composed_gates.n_controlled_X_circuit(qc, [qr[j] for j in range(n - 1)],
                                          qr[n - 1],
                                          [qr[j] for j in range(n, 2 * n - 1)])
    qc.h(qr[n - 1])


def negating_1111(n, qc, qr):
    qc.h(qr[n - 1])
    # To implement 1111 exactly (and not also 1110), we should have a ccx(qr[1], 2, 3, 4)
    # qc.ccx(qr[1], qr[2], qr[3])
    # Target is on qr[3], ancillas are qr[4]...qr[6]
    composed_gates.n_controlled_X_circuit(qc, [qr[j] for j in range(n - 1)],
                                          qr[n - 1],
                                          [qr[j] for j in range(n, 2 * n - 1)])
    qc.h(qr[n - 1])


def negating_00(qc, qr):
    print("negating special state 00")
    qc.x(qr)
    qc.h(qr[1])
    qc.cx(qr[0], qr[1])
    qc.h(qr[1])
    qc.x(qr)


def negating_01(qc, qr):
    print("negating special state 01")
    qc.h(qr[0])
    qc.x(qr[1])
    qc.cx(qr[1], qr[0])
    qc.h(qr[0])
    qc.x(qr[1])


def negating_10(qc, qr):
    print("negating special state 10")
    qc.x(qr[0])

    qc.h(qr[1])
    qc.cx(qr[0], qr[1])
    qc.h(qr[1])

    qc.x(qr[0])


def negating_11(qc, qr):
    print("negating special state 11")
    qc.h(qr[1])
    qc.cx(qr[0], qr[1])
    qc.h(qr[1])


def negating_000(qc, qr):
    print("negating special state 000")
    qc.x(qr)
    qc.h(qr[2])
    qc.ccx(qr[0], qr[1], qr[2])
    qc.h(qr[2])
    qc.x(qr)


def negating_001(qc, qr):
    print("negating special state 001")
    qc.x(qr[0])
    qc.x(qr[1])
    qc.h(qr[2])
    qc.ccx(qr[0], qr[1], qr[2])
    qc.h(qr[2])
    qc.x(qr[1])
    qc.x(qr[0])


def negating_010(qc, qr):
    print("negating special state 010")
    qc.x(qr[0])
    qc.x(qr[2])
    qc.h(qr[1])
    qc.ccx(qr[0], qr[2], qr[1])
    qc.h(qr[1])
    qc.x(qr[0])
    qc.x(qr[2])


def negating_011(qc, qr):
    print("negating special state 011")
    qc.x(qr[0])
    qc.h(qr[2])
    qc.ccx(qr[0], qr[1], qr[2])
    qc.h(qr[2])
    qc.x(qr[0])


def negating_100(qc, qr):
    print("negating special state 100")
    qc.x(qr[1])
    qc.x(qr[2])
    qc.h(qr[0])
    qc.ccx(qr[1], qr[2], qr[0])
    qc.h(qr[0])
    qc.x(qr[1])
    qc.x(qr[2])


def negating_101(qc, qr):
    print("negating special state 101")
    qc.x(qr[1])
    qc.h(qr[1])
    qc.ccx(qr[0], qr[2], qr[1])
    qc.h(qr[1])
    qc.x(qr[1])


def negating_110(qc, qr):
    print("negating special state 110")
    qc.x(qr[2])
    qc.h(qr[0])
    qc.ccx(qr[1], qr[2], qr[0])
    qc.h(qr[0])
    qc.x(qr[2])


def negating_111(qc, qr):
    print("negating special state 111")
    qc.h(qr[2])
    qc.ccx(qr[0], qr[1], qr[2])
    qc.h(qr[2])
