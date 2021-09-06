# ref: https://matplotlib.org/stable/gallery/ticks_and_spines/multiple_yaxis_with_spines.html

import matplotlib.pyplot as plt

fig, ax = plt.subplots(num='123')

p1, = ax.plot([0, 1, 2], [0, 1, 2], "b-", label="Density")

ax.set_xlim(0, 2)
ax.set_ylim(0, 2)

ax.set_xlabel("Distance")
ax.set_ylabel("Density")

ax.yaxis.label.set_color(p1.get_color())

tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)

ax.legend(handles=[p1])

x = ax.scatter(x=[0.5, 1.5], y=[0.6, 1.6], s=25, c='green', marker='^')

plt.pause(1.0)

x.remove()

plt.pause(1.0)

# plt.show()
