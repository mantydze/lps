""" mpiexec -n 4 python3 task_mpi.py
"""
from __future__ import print_function
import time
import numpy as np
from mpi4py import MPI
from task import worker

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

SHAPE = (100, 100, 1000)

t1 = None
jobs = None
if rank == 0:
    # Create jobs: split matrix into (almost) equal partitions
    t1 = time.time()
    M = np.random.randint(10**10, size=SHAPE)
    jobs = np.array_split(M, size)

job = comm.scatter(jobs, root=0)

print("%d rank :: received job" % rank)
result = worker(job)
print("%d rank :: send result" % rank)

results = comm.gather(result, root=0)

if rank == 0:

    result = {
        "_min": min(r["_min"] for r in results),
        "_max": max(r["_max"] for r in results)
    }

    print(result)
    print(time.time() - t1)
