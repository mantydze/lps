import json
import matplotlib.pyplot as plt

data = {}
with open("performance.json", "r") as f:
    data = json.load(f)

fig, axes = plt.subplots(2, sharex=True)

max_nproc = 0

for matrix_performance in data:
    shape = matrix_performance["shape"]
    x = []
    y1 = [] # Seconds
    y2 = [] # Acceleration coeficient
    y0 = None # Time taken with single processor
    yerr = []
    for performance in matrix_performance["performance"]:
        nproc = performance["nproc"]
        max_nproc = max(max_nproc, nproc)
        durations = performance["durations"]
        avg_duration = sum(durations) / len(durations)
        err = max(durations) - min(durations)

        x.append(nproc)
        y1.append(avg_duration)
        yerr.append(err)

        # Acceleration coeficient
        y_ = 1

        if y0:
            y_ = y0 / avg_duration
        else:
            y0 = avg_duration

        y2.append(y_)

    axes[0].errorbar(x=x, y=y1, yerr=yerr)
    axes[1].plot(x, y2, label="shape=%s" % shape)

axes[0].grid()
axes[1].grid()
axes[0].set_ylabel("Sekundes")
axes[1].set_ylabel("Spartinimo koeficientas")

plt.xlabel("Procesoriai")
fig.suptitle("Matricos MinMax")
fig.legend()
plt.show()