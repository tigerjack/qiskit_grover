def n_controlled_X_circuit(qc, controls, target, anc):
    n = len(controls)
    if n == 1:
        qc.cx(controls[0], target)
    elif n == 2:
        qc.ccx(controls[0], controls[1], target)
    else:
        n = len(controls)
        # compute
        qc.ccx(controls[0], controls[1], anc[0])
        for i in range(2, n):
            qc.ccx(controls[i], anc[i - 2], anc[i - 1])
        # copy
        qc.cx(anc[n - 2], target)
        # uncompute
        for i in range(n - 1, 1, -1):
            qc.ccx(controls[i], anc[i - 2], anc[i - 1])
        qc.ccx(controls[0], controls[1], anc[0])


def n_controlled_Z_circuit(qc, controls, target, anc):
    """
    Build a multi-controlled Z circuit w/ a variable number of control qubits and just one target.
    """
    # if (len(controls) > 2):
    #     raise ValueError(
    #         "At the moment, the CZ should have at most 2 control qubits")
    qc.h(target)
    n_controlled_X_circuit(qc, controls, target, anc)
    qc.h(target)
