circuit = None
oracle_simple = None
execute = None
Aer = None
IBMQ = None
least_busy = None


def _import_modules():
    print("Importing modules")
    global circuit, oracle_simple, execute, Aer, IBMQ, least_busy
    import circuit
    import oracle_simple
    from qiskit import execute
    from qiskit import IBMQ, Aer
    from qiskit.backends.ibmq import least_busy


# To be used from REPL
def build_and_infos(n, x_stars, real=False, online=False, backend_name=None):
    _import_modules()
    oracles = []
    for i in range(len(x_stars)):
        oracles.append(oracle_simple.OracleSimple(n, x_stars[i]))
    gc, n_qubits = circuit.get_circuit(n, oracles)
    backend, max_credits, shots = get_appropriate_backend(
        n_qubits, real, online, backend_name)
    res = get_compiled_circuit_infos(gc, backend, max_credits, shots)
    return res


# To be used from REPL
def build_and_run(n, x_stars, real=False, online=False, backend_name=None):
    """
    This just build the grover circuit for the specific n and x_star
    and run them on the selected backend.
    It may be convenient to use in an interactive shell for quick testing.
    """
    _import_modules()
    oracles = []
    for i in range(len(x_stars)):
        oracles.append(oracle_simple.OracleSimple(n, x_stars[i]))
    gc = circuit.get_circuit(n, oracles)
    backend, max_credits, shots = get_appropriate_backend(
        n, real, online, backend_name)
    return run_grover_algorithm(gc, backend, max_credits, shots)


def get_appropriate_backend(n, real, online, backend_name):
    if (not online):
        print("Local simulator backend")
        backend = Aer.get_backend('qasm_simulator')
        max_credits = 10
        shots = 4098
    # Online, real or simuator?
    else:
        print("Online {0} backend".format("real" if real else "simulator"))
        max_credits = 3
        shots = 4098
        IBMQ.load_accounts()
        if (backend_name is not None):
            backend = IBMQ.get_backend(backend_name)
        else:
            large_enough_devices = IBMQ.backends(
                filters=
                lambda x: x.configuration()['n_qubits'] >= n and x.configuration()['simulator'] == (not real)
            )
            backend = least_busy(large_enough_devices)

    print("Backend name is {0}; max_credits = {1}, shots = {2}".format(
        backend, max_credits, shots))
    return backend, max_credits, shots


def get_compiled_circuit_infos(qc, backend, max_credits, shots):
    result = {}
    print("Getting infos ... ")
    backend_coupling = backend.configuration()['coupling_map']
    from qiskit import compile
    grover_compiled = compile(
        qc, backend=backend, coupling_map=backend_coupling, shots=shots)
    grover_compiled_qasm = grover_compiled.experiments[
        0].header.compiled_circuit_qasm
    result['n_gates'] = len(grover_compiled_qasm.split("\n")) - 4
    return result


def run_grover_algorithm(qc, backend, max_credits, shots):
    """
    Run the grover algorithm, i.e. the quantum circuit qc.

    :param qc: The (qiskit) quantum circuit
    :param real: False (default) to run the circuit on a simulator backend, True to run on a real backend
    :param backend_name: None (default) to run the circuit on the default backend (local qasm for simulation, least busy IBMQ device for a real backend); otherwise, it should contain the name of the backend you want to use.
    :returns: Result of the computations, i.e. the dictionary of result counts for an execution.
    :rtype: dict
    """

    _import_modules()
    pending_jobs = backend.status()['pending_jobs']
    print("Backend has {0} pending jobs".format(pending_jobs))

    print("Compiling ... ")
    job = execute(qc, backend, shots=shots, max_credits=max_credits)
    print("Job id is {0}".format(job.job_id()))
    print(
        "At this point, if any error occurs, you can always retrieve the job results using the backend name and the job id using the utils/retrieve_job_results.py script"
    )
    if pending_jobs > 1:
        s = input(
            "Do you want to wait for the job to go up in the queue list or exit the program(q)? If you exit now you can still retrieve the job results later on using the backend name and the job id w/ the utils/retrieve_job_results.py script"
        )
        if (s == "q"):
            print(
                "WARNING: Take note of backend name and job id to retrieve the job"
            )
            from sys import exit
            exit()
    result = job.result()
    return result.get_counts(qc)


def get_max_key_value(counts):
    mx = max(counts.keys(), key=(lambda key: counts[key]))
    total = sum(counts.values())

    confidence = counts[mx] / total
    return mx, confidence


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Grover algorithm")
    parser.add_argument(
        'n',
        metavar='n',
        type=int,
        help='the number of bits used to store the oracle data.')
    parser.add_argument(
        'x_stars',
        metavar='x_star',
        type=int,
        nargs='+',
        help=
        'the number(s) for which the oracle returns 1, in the range [0..2**n-1].'
    )
    parser.add_argument(
        '-r',
        '--real',
        action='store_true',
        help='Invoke the real device (implies -o). Default is simulator.')
    parser.add_argument(
        '-o',
        '--online',
        action='store_true',
        help=
        'Use the online IBMQ devices. Default is local (simulator). This option is automatically set when we want to use a real device (see -r).'
    )
    parser.add_argument(
        '-i',
        '--infos',
        action='store_true',
        help=
        'Print only infos on the circuit built for the specific backend (such as the number of gates) without executing it.'
    )
    parser.add_argument(
        '-b',
        '--backend_name',
        help=
        "The name of the backend. It makes sense only for online ibmq devices and it's useless otherwise. If not specified, the program automatically choose the least busy ibmq backend."
    )
    parser.add_argument(
        '--img_dir',
        help=
        'If you want to store the image of the circuit, you need to specify the directory.'
    )
    parser.add_argument(
        '--plot',
        action='store_true',
        help='Plot the histogram of the results. Default is false')
    args = parser.parse_args()
    n = args.n
    x_stars = args.x_stars
    print("n: {0}, x_stars: {1}".format(n, x_stars))
    real = args.real
    online = True if real else args.online
    infos = args.infos
    backend_name = args.backend_name
    img_dir = args.img_dir
    plot = args.plot
    print("real: {0}, online: {1}, infos: {2}, backend_name: {3}".format(
        real, online, infos, backend_name))

    _import_modules()

    oracles = []
    for i in range(len(x_stars)):
        oracles.append(oracle_simple.OracleSimple(n, x_stars[i]))
    gc, n_qubits = circuit.get_circuit(n, oracles)

    if (img_dir is not None):
        from qiskit.tools.visualization import circuit_drawer
        circuit_drawer(
            gc, filename=img_dir + "grover_{0}_{1}.png".format(n, x_stars[0]))

    backend, max_credits, shots = get_appropriate_backend(
        n_qubits, real, online, backend_name)
    if (infos):
        res = get_compiled_circuit_infos(gc, backend, max_credits, shots)
        for k, v in res.items():
            print("{0} --> {1}".format(k, v))
    else:  #execute
        counts = run_grover_algorithm(gc, backend, max_credits, shots)
        print(counts)
        max, confidence = get_max_key_value(counts)
        print("Max value: {0}, confidence {1}".format(max, confidence))
        if (plot):
            from qiskit.tools.visualization import plot_histogram
            plot_histogram(counts)
    print("END")


# Assumption: if run from console we're inside src/.. dir
if __name__ == "__main__":
    main()
