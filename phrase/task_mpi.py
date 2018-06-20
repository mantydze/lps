""" mpiexec -n 4 python3 task_mpi.py "Labadiena Lietuva"
"""
from __future__ import print_function
import sys
import time
import numpy as np
from mpi4py import MPI
from task import initial_population, calc_fitness, evolve

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

TARGET = sys.argv[1] if len(sys.argv)>1 else "Monika yra pasiutus ir niekada nemiega"

t1 = None # Start time
population = None # Initial population
found = False

if rank == 0:
    t1 = time.time()
    population = initial_population(len(TARGET), 100)

while not found:
    # Broadcast same population to all processes
    population = comm.bcast(population, root=0)

    print("%d rank :: received job" % rank)
    # Do actual work: breed, mutate
    found_, population = evolve(population, TARGET, verbose=False)
    result = {"found": found_, "population": population}
    print("%d rank :: send result" % rank)
    # Send result to master
    results = comm.gather(result, root=0)

    if rank == 0:
        print("*"*80)
        populations = []
        # Accumulate populations from all processes
        for index, result in enumerate(results):
            found = max(found, result["found"])
            print("%d :: %s" % (index, result["found"]))
            populations += result["population"]

        if found:
            print(time.time() - t1)
        else:
            # Sort by fitness score and select only best ones for next iteration
            fitness = calc_fitness(populations, TARGET)
            fitness.sort(key=lambda x:x[1], reverse=True)
            population = [f[0] for f in fitness][:len(population)]
            print("Best ::", fitness[0])
            # print(population)

    comm.barrier()
    found = comm.bcast(found, root=0)
