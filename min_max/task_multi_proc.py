import time
import json
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from task import worker

def find(M, nproc=1):
    """
        M - 3 dimentional numpy array
        nproc - number of processes
    """

    jobs = np.array_split(M, nproc)

    with ProcessPoolExecutor(nproc) as pool:
        results = list(pool.map(worker, jobs))

        result= None
        result = {
            "_min": min(r["_min"] for r in results),
            "_max": max(r["_max"] for r in results)
        }

    return result

if __name__ == '__main__':
    print("GO!")

    SHAPE = (10, 100, 100)
    N_PROC = 8     # number of parallel processes
    N_REPEAT = 5    # number of times to repeat task with n processes

    performance = []

    for SHAPE in [(100, 100, 100), (100, 100, 200), (100, 200, 200), (200, 200, 200), (300, 300, 300)]:
        performance_ = []
        M = np.random.randint(10**10, size=SHAPE)
        for nproc in range(1, N_PROC):

            durations = []
            for _ in range(N_REPEAT):
                t1 = time.time()
                find(M, nproc)
                t2 = time.time()
                diff = t2 - t1

                print("%d proc :: %02f sec" % (nproc, diff))

                durations.append(diff)

            performance_.append({"nproc": nproc, "durations": durations})
        performance.append({"shape": SHAPE, "performance": performance_})

    performance_json = json.dumps(performance, indent=4)
    print(performance_json)

    with open("performance.json", "w") as f:
        f.write(performance_json)
