from math import sin
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
import pandas as pd
import numpy as np

x = list()
y = list()
start = 0  # to avoid warning from PyCharm
time_end = int(input("Insert how long simulation should be working: "))
# Arduino reference:
my_board = serial.Serial()
my_board.port = "COM4"
my_board.baudrate = 9600
# my_board.open()
name_of_file = time.strftime("Day-%d-%m-%Y_Hour-%H-%M-%S")

# explanation of "fig, ax...":
# https://stackoverflow.com/questions/34162443/why-do-many-examples-use-fig-ax-plt-subplots-in-matplotlib-pyplot-python

# explanation of "ln,": https://stackoverflow.com/questions/65337288/line-ax-plotx-y
fig, ax = plt.subplots()
ax.autoscale_view()
(ln,) = ax.plot(x, y)
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title("Signal")
ax.set_xlim([0, time_end])
plt.grid()


def animate(i):
    global start
    if i == 0:
        start = time.time()  # to subtract beginning time
    data_t = time.time() - start
    x.append(data_t)
    # replace code below with arduino data y.append(arduino_data)
    # arduino_data = str(my_board.readline())
    # a_data = int(arduino_data[2:][:-5])
    # y.append(a_data)
    gain = 0.05  # noise amp.
    noise = gain * np.random.normal(0, 1, 1)
    y.append(sin(data_t + noise))  # simulate signal of arduino input

    # arduino up there
    ln.set_data(x, y)
    if min(y) == max(y):
        ax.set_ylim([-1, max(y) + 0.01])
    else:
        ax.set_ylim([min(y) - 0.01, max(y) + 0.01])
    if x[-1] > time_end:
        ani.event_source.stop()
        # save plot as image:
        name = name_of_file + ".png"
        plt.savefig(name)


ani = FuncAnimation(fig, animate, interval=0.01, frames=time_end * 1000 * 1000)

# show output:
plt.show()
# save data to file:
filename = name_of_file + ".txt"
file = open(filename, "a")
file.write(time.ctime() + "\n")
container = {"Time": x, "Values": y}
signal_data = pd.DataFrame(container).to_string(index=False)
file.write(signal_data)
file.write("\n")
file.close()

# making gif of output:
fig2, ax2 = plt.subplots()
ax2.autoscale_view()
(ln2,) = ax2.plot(x, y)
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title("Signal")
ax2.set_xlim([0, time_end])
ax2.set_ylim([min(y) - 0.01, max(y) + 0.01])
plt.grid()

x1 = list()
y1 = list()


def make_me_gif(i):
    x1.append(x[i])
    y1.append(y[i])
    ln2.set_data(x1, y1)


gif = FuncAnimation(fig2, make_me_gif, interval=0.01, frames=len(x))
gifName = name_of_file + ".gif"
gif.save(gifName)
