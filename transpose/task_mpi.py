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

N = 4000 # Matrix size
M = None # Original Matrix (created by root proc)
t1 = None # Start time
jobs = None # Jobs for workers (splitted matrix) in to (almost) equal parts

if rank == 0:
    t1 = time.time()
    M = np.random.randint(10, size=(N, N))
    jobs = np.array_split(M, size, axis=1)

job = comm.scatter(jobs, root=0)

print("%d rank :: received job" % rank)
result = worker(job)
print("%d rank :: send result" % rank)

results = comm.gather(result, root=0)

if rank == 0:
    T = np.stack(np.concatenate(results))
    assert np.allclose(T, M.transpose()), "Transposed matrix incorrect"
    print(time.time() - t1)
