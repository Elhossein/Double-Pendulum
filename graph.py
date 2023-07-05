import matplotlib.pyplot as plt
import csv

degs = [30]

for deg in degs:

    fig = plt.figure(figsize=(11, 5))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    # data = open('data_%s.csv'%deg,'r').read()
    # lines = data.split('\n')

    t = []
    theta1 = []
    theta2 = []

    with open('data_th1_30_%s.csv'%deg) as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            t.append(float(row[0]))
            theta1.append(float(row[1]))
            theta2.append(float(row[2]))

    d = 2500
    # t = [t[i+d] for i in range(0, 50000-d, d)]
    # theta1 = [sum(theta1[i:i+d])/d for i in range(0, 50000-d, d)]
    # theta2 = [sum(theta2[i:i+d])/d for i in range(0, 50000-d, d)]
    theta1 = theta1[:d]
    theta2 = theta2[:d]
    t = [i + 500 for i in t[:d]]
    dtheta = [abs(i - j) for i, j in zip(theta1, theta2)]

    ax1.plot(t, theta1)
    ax1.plot(t, theta2)

    ax1.legend(['Pendulum 1', 'Pendulum 2'], loc='upper left')

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel(r'${\Theta_2}$ (rad)')
    ax1.set_title(r'Time Vs. ${\Theta_2}$')	

    ax2.plot(t, dtheta, c="r")

    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel(r'${\Delta\Theta_2}$ (rad)')
    ax2.set_title(r'Time Vs. ${\Delta\Theta_2}$')	
        
    plt.savefig('Graph_th1_%s'%deg)


    # fig = plt.figure(figsize=(6, 6))
    # ax = fig.add_subplot(111, projection='3d')

    # ax.plot(theta1, theta2, t)

    # plt.savefig('Graph_th2_%s_2'%deg)

plt.show()