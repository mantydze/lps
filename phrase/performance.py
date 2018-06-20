import os
import time
import json

N_PROC = 8    # number of parallel processes
N_REPEAT = 5  # number of times to repeat task with n processes
performance = []

# 40, 80, 120
phrases = [
    "Monika yra pasiutus ir niekada nemiega!!",
    "Monika yra pasiutus ir niekada nemiega!!"*2,
    "Monika yra pasiutus ir niekada nemiega!!"*3,
]

for phrase in phrases:
    performance_ = []
    for nproc in range(1, N_PROC):
        durations = []
        for _ in range(N_REPEAT):
            print("********************* REPEAT *********************")
            t1 = time.time()
            p = os.popen("mpiexec -n %d python3 task_mpi.py '%s'" % (nproc, phrase))
            out = p.read()
            p.close()
            print(out)
            t2 = time.time()
            diff = t2 - t1

            print("%d proc :: %02f sec" % (nproc, diff))

            durations.append(diff)

        performance_.append({"nproc": nproc, "durations": durations})

    performance.append({"L": len(phrase), "performance": performance_})

performance_json = json.dumps(performance, indent=4)
print(performance_json)

with open("performance.json", "w") as f:
    f.write(performance_json)