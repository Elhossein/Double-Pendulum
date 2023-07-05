import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from pendulum import DoublePendulum
from time import time
import csv, sys
# from numpy import arctan

deg = 120
fps = 60
seconds = 40
trail = -80
dt = 1./fps
total_frames = seconds * fps

pendulum1 = DoublePendulum([-100, 0.0, deg, 0.0])
pendulum2 = DoublePendulum([-100, 0.0, deg + 0.001, 0.0])
pendulum1.step(dt)
pendulum2.step(dt)


fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                    xlim=(-2, 2), ylim=(-2, 2))
c = sns.hls_palette(8, l=.3, s=.8)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Double Pendulum')

line1, = ax.plot([], [], "-o", color='k', linestyle='-', linewidth=2)
line2, = ax.plot([], [], "-o", color='k', linestyle='-', linewidth=2)
dot, = ax.plot([], [], 'o', color='k', markersize = 10)
dot1_1, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = 12, markerfacecolor = '#0077BE',lw=2, markevery=10000, markeredgecolor = 'k')   # line for Earth
dot2_1, = ax.plot([], [], 'o-',color = '#ffebd8',markersize = 12, markerfacecolor = '#f66338',lw=2, markevery=10000, markeredgecolor = 'k')
dot1_2, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = 12, markerfacecolor = '#0077BE',lw=2, markevery=10000, markeredgecolor = 'k')   # line for Earth
dot2_2, = ax.plot([], [], 'o-',color = '#ffebd8',markersize = 12, markerfacecolor = '#f66338',lw=2, markevery=10000, markeredgecolor = 'k')
track1, = ax.plot([], [], color="#0077BE", linewidth=2)
track2, = ax.plot([], [], color="#f66338", linewidth=2)

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

x1 = []
y1 = []
x2 = []
y2 = []
th1 = []
th2 = []
t = 0
t_list = []

def init():
    """initialize animation"""
    line1.set_data([], [])
    line2.set_data([], [])

    track1.set_data([], [])
    track2.set_data([], [])

    dot.set_data([], [])
    dot1_1.set_data([], [])
    dot1_2.set_data([], [])
    dot2_1.set_data([], [])
    dot2_2.set_data([], [])

    time_text.set_text('')
    return line1, line2, track1, track2, time_text, dot, dot1_1, dot1_2, dot2_1, dot2_2

def animate(i):
    """perform animation step"""
    global pendulum1, pendulum2, dt, t
    pendulum1.step(dt)
    pendulum2.step(dt)
    line1.set_data(*pendulum1.position())
    line2.set_data(*pendulum2.position())

    pos1 = pendulum1.position()
    pos2 = pendulum2.position()

    dot.set_data([0, 0], [0, 0])
    dot1_1.set_data(pos1[0][1], pos1[1][1])
    dot1_2.set_data(pos1[0][2], pos1[1][2])
    dot2_1.set_data(pos2[0][1], pos2[1][1])
    dot2_2.set_data(pos2[0][2], pos2[1][2])

    t += dt
    t_list.append(t)
    th1.append(pendulum1.state[2])
    th2.append(pendulum2.state[2])

    time_text.set_text('time = %.1f' % pendulum1.time_elapsed)

    x1.append(pendulum1.position()[0][2])
    y1.append(pendulum1.position()[1][2])
    track1.set_data(x1[trail:i], y1[trail:i])
    x2.append(pendulum2.position()[0][2])
    y2.append(pendulum2.position()[1][2])
    track2.set_data(x2[trail:i], y2[trail:i])
    sys.stdout.write("\rframe {0}/{1}".format(i, total_frames))
    sys.stdout.flush()

    return line1, line2, track1, track2, time_text, dot, dot1_1, dot1_2, dot2_1, dot2_2

# choose the interval based on dt and the time to animate one step

t0 = time()
animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)

anim = animation.FuncAnimation(fig, animate, frames=int(seconds/dt), blit=True, init_func=init, interval=interval)
plt.show()
anim.save('animation.gif', fps=1/dt, writer = 'imagemagick')
