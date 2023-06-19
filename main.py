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
my_board.port = 'COM4'
my_board.baudrate = 9600

# explanation of "fig, ax...":
# https://stackoverflow.com/questions/34162443/why-do-many-examples-use-fig-ax-plt-subplots-in-matplotlib-pyplot-python

# explanation of "ln,": https://stackoverflow.com/questions/65337288/line-ax-plotx-y
fig, ax = plt.subplots()
ax.autoscale_view()
ln, = ax.plot(x, y)
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.title('Signal')
ax.set_xlim([0, time_end])
plt.grid()


def animate(i):
    global start
    if i == 0:
        start = time.time()  # to subtract beginning time
    data_t = time.time() - start
    x.append(data_t)  # time.process_time()-start
    # replace code below with arduino data y.append(arduino_data)
    gain = 0.05  # noise amp.
    noise = gain * np.random.normal(0, 1, 1)
    y.append(sin(data_t + noise))
    # arduino up there
    ln.set_data(x, y)
    if min(y) == max(y):
        ax.set_ylim([-1, max(y)])
    else:
        ax.set_ylim([min(y), max(y)])
    if x[-1] > time_end:
        ani.event_source.stop()


ani = FuncAnimation(fig, animate, interval=0.01, frames=time_end * 1000 * 1000)
plt.show()

file = open('Data.txt', 'a')
file.write(time.ctime() + '\n')

container = {'Time': x, 'Values': y}
signal_data = pd.DataFrame(container).to_string(index=False)
file.write(signal_data)
file.write('\n')
file.close()
