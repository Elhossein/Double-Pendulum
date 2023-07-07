import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import numpy as np
from seaborn import hls_palette
from pendulum import DoublePendulum
from time import time
import warnings

warnings.filterwarnings("ignore")

fps = 30 # frame per second
seconds = 40 # duration of animation in seconds

deg = 120 # initial angle of pendulum in degrees
trail = 40 # number of previous positions to draw
dt = 1./fps # time step
total_frames = seconds * fps # total number of frames to compute

pendulum1 = DoublePendulum([-100, 0.0, deg, 0.0]) # pendulum 1
pendulum2 = DoublePendulum([-100, 0.0, deg + 0.0001, 0.0]) # pendulum 2
pendulum1.step(dt) # step once to compute the initial position
pendulum2.step(dt) # step once to compute the initial position


fig = plt.figure() # make figure
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))   # add to figure
c = hls_palette(8, l=.3, s=.8) # color palette
ax.grid(False)  # no grid
ax.set_xticks([]) # no ticks
ax.set_yticks([]) # no ticks
ax.set_title('Two Double Pendulums') # title

line1, = ax.plot([], [], "-o", color='k', linestyle='-', linewidth=2)  # line for pendulum 1
line2, = ax.plot([], [], "-o", color='k', linestyle='-', linewidth=2)  # line for pendulum 2
dot, = ax.plot([], [], 'o', color='k', markersize = 10) # dot at origin
dot1_1, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = 12, markerfacecolor = '#0077BE',lw=2, markevery=10000, markeredgecolor = 'k')  
dot2_1, = ax.plot([], [], 'o-',color = '#ffebd8',markersize = 12, markerfacecolor = '#f66338',lw=2, markevery=10000, markeredgecolor = 'k')
dot1_2, = ax.plot([], [], 'o-',color = '#d2eeff',markersize = 12, markerfacecolor = '#0077BE',lw=2, markevery=10000, markeredgecolor = 'k') 
dot2_2, = ax.plot([], [], 'o-',color = '#ffebd8',markersize = 12, markerfacecolor = '#f66338',lw=2, markevery=10000, markeredgecolor = 'k')
track1, = ax.plot([], [], color="#0077BE", linewidth=2) # trail for pendulum 1
track2, = ax.plot([], [], color="#f66338", linewidth=2) # trail for pendulum 2

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes) # text for displaying the time

A = np.zeros((2, 2, total_frames)) # array for storing positions of both pendulums
t = 0

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
    global pendulum1, pendulum2, dt, t # declare as globals

    pendulum1.step(dt)
    x1 = pendulum1.get_x() 
    y1 = pendulum1.get_y()
    pendulum2.step(dt)
    x2 = pendulum2.get_x()
    y2 = pendulum2.get_y()
    
    line1.set_data(x1, y1)
    line2.set_data(x2, y2)


    dot.set_data([0, 0], [0, 0])
    dot1_1.set_data(x1[1], y1[1])
    dot1_2.set_data(x1[2], y1[2])
    dot2_1.set_data(x2[1], y2[1])
    dot2_2.set_data(x2[2], y2[2])

    t += dt  # increment time

    time_text.set_text('time = %.1f' % pendulum1.time_elapsed)
    A[0, 0, i] = x1[2] # store the current positions into the arrays
    A[0, 1, i] = y1[2] 
    A[1, 0, i] = x2[2]  
    A[1, 1, i] = y2[2]
    track1.set_data(A[0, 0, i:max(1,i-trail):-1], A[0, 1, i:max(1,i-trail):-1]) # set the trailing points 
    track2.set_data(A[1, 0, i:max(1,i-trail):-1], A[1, 1, i:max(1,i-trail):-1])
    sys.stdout.write("\rframe {0}/{1}".format(i, total_frames)) # write out the frame number to stdout
    sys.stdout.flush() # flush stdout (necessary for running from Spyder)

    return line1, line2, track1, track2, time_text, dot, dot1_1, dot1_2, dot2_1, dot2_2



t0 = time()  
animate(0)  
t1 = time()  
interval = 1000 * dt - (t1 - t0)   # subtract time already spent on drawing from the time interval
anim = animation.FuncAnimation(fig, animate, init_func=init,frames=range(1, total_frames), interval=interval, blit=True)   # animate
anim.save('animation.gif', fps=fps, writer = 'imagemagick')  # save animation as gif
plt.close()