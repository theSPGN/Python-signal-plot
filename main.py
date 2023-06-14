from math import sin
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
import pandas as pd

# pomysł:
# wał złączony z silnikiem prądu stałego posiada w odległości d/2 (od osi) naklejkę, która będzie wykrywana
# przez czujnik laserowy, który wysyła informację binarną do programu poprzez płytkę arduino uno (klon arduino)
# odstęp między kolejnymi impulsami (tj. pojawieniem się 1 na wejściu) oznacza okres (T = x milisekund)
# z okresu wyznaczamy prędkość kątową omega = 2PI/T
# z prędkości kątowej można wyznaczyć prędkość styczną v = omega*r i ew. inne jakieś parametry prędkość obr n=1/T itd.


x = list()
y = list()
start = 0  # to avoid warning from PyCharm
time_end = int(input("Insert how long simulation should be working: "))
sample_time = int(input('Sample time interval in ms: '))
# tutaj arduno ogarnąć i wgl:
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
        start = time.process_time()  # to subtract beginning time

    x.append(time.process_time() - start)  # time.process_time()-start
    time.sleep(sample_time / 1000)
    # do zamiany na inf z arduino:
    y.append(sin(time.process_time() - start))
    ln.set_data(x, y)
    if min(y) == max(y):
        ax.set_ylim([-1, max(y)])
    else:
        ax.set_ylim([min(y), max(y)])
    if x[-1] > time_end:
        ani.event_source.stop()


ani = FuncAnimation(fig, animate, interval=0, frames=time_end * sample_time * 1000)
plt.show()

file = open('Data.txt', 'a')
file.write(time.ctime() + '\n')

container = {'Time': x, 'Values': y}
signal_data = pd.DataFrame(container).to_string(index=False)
file.write(signal_data)
file.write('\n')
file.close()
