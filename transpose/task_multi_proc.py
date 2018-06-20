import time
import json
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from task import worker

def transpose(M, nproc=1):
    jobs = np.array_split(M, nproc, axis=1)

    with ProcessPoolExecutor(nproc) as pool:
        results = list(pool.map(worker, jobs))
        T = np.stack(np.concatenate(results))

    assert np.allclose(T, M.transpose()), "Transposed matrix incorrect"

if __name__ == '__main__':

    # N = 4000
    N_PROC = 8    # number of parallel processes
    N_REPEAT = 5  # number of times to repeat task with n processes
    performance = []

    for N in [1000, 2000, 3000, 4000, 5000, 6000]:
        M = np.random.randint(10, size=(N, N))
        performance_ = []
        for nproc in range(1, N_PROC):

            durations = []
            for _ in range(N_REPEAT):
                t1 = time.time()
                transpose(M, nproc)
                t2 = time.time()
                diff = t2 - t1

                print("%d proc :: %02f sec" % (nproc, diff))

                durations.append(diff)

            performance_.append({"nproc": nproc, "durations": durations})

        performance.append({"N": N, "performance": performance_})

    performance_json = json.dumps(performance, indent=4)
    # print(performance_json)

    with open("performance.json", "w") as f:
        f.write(performance_json)
