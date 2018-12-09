from qiskit import IBMQ
import sys


def get_job_status(backend, job_id):
    backend = IBMQ.get_backend(backend)
    print("Backend {0} is operational? {1}".format(
        backend.name(),
        backend.status()['operational']))
    print("Backend was last updated in {0}".format(
        backend.properties()['last_update_date']))
    print("Backend has {0} pending jobs".format(
        backend.status()['pending_jobs']))
    ibmq_job = backend.retrieve_job(job_id)
    status = ibmq_job.status()
    print(status.name)
    print(ibmq_job.creation_date())
    if (status.name == 'DONE'):
        print("EUREKA")
        result = ibmq_job.result()
        count = result.get_counts()
        print("Result is: {0}".format())
        from qiskit.tools.visualization import plot_histogram
        plot_histogram(counts)
    else:
        print("... Work in progress ...")
        print("Queue position = {0}".format(ibmq_job.queue_position()))
        print("Error message = {0}".format(ibmq_job.error_message()))


IBMQ.load_accounts()
print("Account(s) loaded")

if (len(sys.argv) > 2):
    get_job_status(sys.argv[1], sys.argv[2])
