import quantum_negating_basis_states as qnbs
import oracle_abstract


class OracleSimple(oracle_abstract.Oracle):
    """
    A simple oracle which uses a quantum circuit composed by CNOT and H gates
    to implement the Oracle.
    """

    def get_circuit(self, qr, qc):
        # if (self.n > 3):
        #     raise ValueError(
        #         "At the moment, the oracle works with up to 3 qubits")
        if (self.x_star >= 2**self.n):
            raise ValueError("x_star should be b/w 0 and 2**n - 1")
        qnbs.negating_basis_state(self.n, qc, qr, self.x_star)
