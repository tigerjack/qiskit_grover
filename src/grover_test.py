import circuit
import oracle_simple
from qiskit import execute, Aer
from qiskit.tools.visualization import circuit_drawer
from qiskit.tools.visualization import plot_histogram
from qiskit import IBMQ, compile
from qiskit.backends.ibmq import least_busy
from sys import argv


def draw_circuit(qc, filename):
    """
    Draw the circuit (with the gates) on the given filename
    """
    print("Drawing inside {0}".format(filename))
    circuit_drawer(qc, filename=filename)


def plot_results(counts, filename):
    print("Plotting inside {0}".format(filename))
    plot_histogram(counts)


def get_appropriate_backend(n, real=False, backend_name=None):
    if (not real):
        print("Simulator backend")
        backend = Aer.get_backend('qasm_simulator')
        max_credits = 10
        shots = 4098
    else:
        print("Real backend")
        max_credits = 3
        shots = 4098
        IBMQ.load_accounts()
        if (backend_name is None):
            large_enough_devices = IBMQ.backends(
                filters=
                lambda x: x.configuration()['n_qubits'] >= n and not x.configuration()['simulator']
            )
            backend = least_busy(large_enough_devices)
        else:
            backend = IBMQ.get_backend(backend_name)

    print("Backend name is {0}; max_credits = {1}, shots = {2}".format(
        backend, max_credits, shots))
    return backend, max_credits, shots


def get_compiled_circuit_infos(qc, backend, max_credits, shots):
    result = {}
    print("Getting infos ... ")
    backend_coupling = backend.configuration()['coupling_map']
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

    print("Executing ... ")
    job = execute(qc, backend, shots=shots, max_credits=max_credits)
    print("Job id is {0}".format(job.job_id()))
    print(
        "Note that you can also stop the execution here and retrieve the results later using the previous job id and backend name"
    )
    result = job.result()
    return result.get_counts(qc)


def build_and_run(n, x_star, real, backend_name):
    """
    This just build the grover circuit for the specific n and x_star
    and run them on the selected backend.
    It may be convenient to use in an interactive shell for quick testing.
    """
    oracle = oracle_simple.OracleSimple(n, x_star)
    gc = circuit.get_circuit(n, oracle)
    backend, max_credits, shots = get_appropriate_backend(
        n, real, backend_name)
    return run_grover_algorithm(gc, backend, max_credits, shots)


def usage():
    print("""
    1st parameter is number of qubits; can be 2 or 3 (default 2)
    2nd parameter is x_star; can be b/w 0 and 2**n - 1 (default 3)
    3rd parameter is False (0) for simulator, True (1) for IBMQ real device (default False)
    4th parameter is False (0) for execution, True (1) for just getting circuit infos (default False)
    5th parameter is the name of the backend to use (default is the least busy one)
    """)


def get_max_key_value(counts):
    mx = max(counts.keys(), key=(lambda key: counts[key]))
    total = sum(counts.values())

    confidence = counts[mx] / total
    return mx, confidence


def main(img_dir, plot_dir):
    try:
        backend_name = argv[5] if len(argv) >= 6 else None
        infos = int(argv[4]) == 1 if (len(argv) >= 5) else False
        real = int(argv[3]) == 1 if (len(argv) >= 4) else False
        x_star = int(argv[2]) if (len(argv) >= 3) else 3
        n = int(argv[1]) if (len(argv) >= 2) else 2
    except IndexError:
        print("Wrong number of parameters")
        usage()
        return
    except ValueError:
        print("Wrong value for parameters")
        usage()
        return

    oracle = oracle_simple.OracleSimple(n, x_star)
    gc = circuit.get_circuit(n, oracle)

    if (img_dir is not None):
        draw_circuit(gc, img_dir + "grover_3_{0}_{1}.png".format(n, x_star))

    backend, max_credits, shots = get_appropriate_backend(
        n, real, backend_name)
    if (infos):
        res = get_compiled_circuit_infos(gc, backend, max_credits, shots)
        for k, v in res.items():
            print("{0} --> {1}".format(k, v))

    else:  #execute
        print("Backend has {0} pending jobs".format(
            backend.status()['pending_jobs']))
        counts = run_grover_algorithm(gc, backend, max_credits, shots)
        print(counts)
        max, confidence = get_max_key_value(counts)
        print("Max value: {0}, confidence {1}".format(max, confidence))
        if (plot_dir is not None):
            # Actually you can't plot on a file, so this is useless
            plot_results(
                counts,
                plot_dir + "grover_3_{0}_{1}_{2}.png".format(n, x_star, real))
    print("END")


# Assumption: if run from console we're inside src/.. dir
if __name__ == "__main__":
    #img_dir = "./imgs/"
    #plot_dir = "./plots/"
    #main(img_dir, plot_dir)
    main(None, None)
