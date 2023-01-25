# create and display the animation for the determination test
# needs to take in all the quaternions collected from data

import Rot_functions as Rot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.animation as animation

def test_animation():
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                        init_func=init, blit=True)
    plt.show()


def initialize_cube(l):
    # makes a vector of vertices for a cube of side length l
    cube_vectors = np.zeros([8,3])

    cube_vectors[0,:] = np.array([0,0,0])
    cube_vectors[1,:] = np.array([l,0,0])
    cube_vectors[3,:] = np.array([0,l,0])
    cube_vectors[4,:] = np.array([0,0,l])
    cube_vectors[2,:] = np.array([l,l,0])
    cube_vectors[5,:] = np.array([l,0,l])
    cube_vectors[7,:] = np.array([0,l,l])
    cube_vectors[6,:] = np.array([l,l,l])

    return cube_vectors


def create_animation(quats):

    cube_vecs = initialize_cube(1)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    graph_cube(cube_vecs,ax)

    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    lines = []
    for quat in quats:
        frame = []
        #rotate all the vectors according to the quat
        new_vecs = np.zeros([8,3])
        for i,vec in enumerate(cube_vecs):
            print(vec)
            print(quat[1:])
            new_vecs[i,:] = Rot.quat_rot(float(quat[0]),quat[1:],vec.T)

        frame.extend(graph_cube(new_vecs,ax))
        lines.append(frame)

    anim = animation.ArtistAnimation(fig, lines, interval = 200, blit = True, repeat = True)

    # also make plot of quaternions over time
    fig3 = plt.figure()
    plt.plot(quats)
    plt.title('Quaternions over time')
    plt.legend(['r','i','j','k'])

    plt.show()

def graph_cube(cube_vecs,ax):
    #graphs a cube 

    #X, Y = np.meshgrid(r, r)
    #Z, Y = np.meshgrid(r, r)

    #print(cube_vecs)
    pnt = ax.scatter3D(cube_vecs[:, 0], cube_vecs[:, 1], cube_vecs[:, 2], color='k')

    s1 = ax.plot_surface(np.array([[cube_vecs[0,0],cube_vecs[1,0]],[cube_vecs[3,0],cube_vecs[2,0]]]),np.array([[cube_vecs[0,1],cube_vecs[1,1]],[cube_vecs[3,1],cube_vecs[2,1]]]),np.array([[cube_vecs[0,2],cube_vecs[1,2]],[cube_vecs[3,2],cube_vecs[2,2]]]), alpha=0.7, color='gray')
    s2 = ax.plot_surface(np.array([[cube_vecs[4,0],cube_vecs[5,0]],[cube_vecs[7,0],cube_vecs[6,0]]]),np.array([[cube_vecs[4,1],cube_vecs[5,1]],[cube_vecs[7,1],cube_vecs[6,1]]]),np.array([[cube_vecs[4,2],cube_vecs[5,2]],[cube_vecs[7,2],cube_vecs[6,2]]]), alpha=0.7, color='gray')
    s3 = ax.plot_surface(np.array([[cube_vecs[0,0],cube_vecs[1,0]],[cube_vecs[4,0],cube_vecs[5,0]]]),np.array([[cube_vecs[0,1],cube_vecs[1,1]],[cube_vecs[4,1],cube_vecs[5,1]]]),np.array([[cube_vecs[0,2],cube_vecs[1,2]],[cube_vecs[4,2],cube_vecs[5,2]]]), alpha=0.7, color='gray')
    s4 = ax.plot_surface(np.array([[cube_vecs[2,0],cube_vecs[3,0]],[cube_vecs[6,0],cube_vecs[7,0]]]),np.array([[cube_vecs[2,1],cube_vecs[3,1]],[cube_vecs[6,1],cube_vecs[7,1]]]),np.array([[cube_vecs[2,2],cube_vecs[3,2]],[cube_vecs[6,2],cube_vecs[7,2]]]), alpha=0.7, color='gray')
    s5 = ax.plot_surface(np.array([[cube_vecs[2,0],cube_vecs[6,0]],[cube_vecs[1,0],cube_vecs[5,0]]]),np.array([[cube_vecs[2,1],cube_vecs[6,1]],[cube_vecs[1,1],cube_vecs[5,1]]]),np.array([[cube_vecs[2,2],cube_vecs[6,2]],[cube_vecs[1,2],cube_vecs[5,2]]]), alpha=0.7, color='gray')
    s6 = ax.plot_surface(np.array([[cube_vecs[0,0],cube_vecs[4,0]],[cube_vecs[3,0],cube_vecs[7,0]]]),np.array([[cube_vecs[0,1],cube_vecs[4,1]],[cube_vecs[3,1],cube_vecs[7,1]]]),np.array([[cube_vecs[0,2],cube_vecs[4,2]],[cube_vecs[3,2],cube_vecs[7,2]]]), alpha=0.7, color='gray')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    #basic vectors of the body frame
    v1 = ax.quiver(cube_vecs[0,0],cube_vecs[0,1],cube_vecs[0,2],-(cube_vecs[0,0]-cube_vecs[1,0])/2,-(cube_vecs[0,1]-cube_vecs[1,1])/2,-(cube_vecs[0,2]-cube_vecs[1,2])/2,color='green')
    v2 = ax.quiver(cube_vecs[0,0],cube_vecs[0,1],cube_vecs[0,2],-(cube_vecs[0,0]-cube_vecs[3,0])/2,-(cube_vecs[0,1]-cube_vecs[3,1])/2,-(cube_vecs[0,2]-cube_vecs[3,2])/2,color='green')
    v3 = ax.quiver(cube_vecs[0,0],cube_vecs[0,1],cube_vecs[0,2],-(cube_vecs[0,0]-cube_vecs[4,0])/2,-(cube_vecs[0,1]-cube_vecs[4,1])/2,-(cube_vecs[0,2]-cube_vecs[4,2])/2,color='green')

    return [s1,s2,s3,s4,s5,s6,pnt,v1,v2,v3]

def format_quats(list_quats):
    # takes the list of the r,i,j, and k components and makes a list where each element is a list of all 4 values
    good_quats = []
    rvals = list_quats[0]
    ivals = list_quats[1]
    jvals = list_quats[2]
    kvals = list_quats[3]
    for n in range(len(rvals)-2):
        good_quats.append([float(rvals[n+2]),float(ivals[n+2]),float(jvals[n+2]),float(kvals[n+2])])

    return good_quats
