import numpy as np
import matplotlib.pyplot as plt

"""Defining constants/values"""
q = 1
m = 1   

dt = 0.01
K = 1000 

#defining initial values
x_0 = [1, 0]
v_0 = [0, 1]
#starte def her som tar inn initial values?


""" Defining functions """
#creating a function to produce the rotational matrix
def rotation(t):
    matrix = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    return matrix

def linear_field(pos_0, v_0):
    """ Defining values """
    #creating empty arrays to fill with position and velocity
    position = np.zeros((K+1, 2))  
    velocity = np.zeros((K+1, 2))

    #inputting initial values in the position and velocity arrays
    position[0] = np.array(pos_0) 
    velocity[0] = np.array(v_0)

    #defining electric and magnetic fields
    E = np.zeros((K+1)) #defining only E(x)
    B = 0 #Setting E=0 for this task

    #defining E(x) at t=0 (to E(x) = -x)
    E[0] = -position[0,0]

    #defining theta 
    theta = - ((q * B * dt) / m)


    """Performing the half rotation backwards"""
    #defining the rotational matrix for the half rotation backwards
    theta_back = rotation(- (theta / 2))

    #defining the rotational matrix to be used in the for-loop
    rot_mat = rotation(theta)

    #performing the ACTUAL half rotation backwards
    v_min1 = np.matmul(theta_back, velocity[0])

    #performing the half deceleration
    velocity[0, 0] = v_min1[0] - ((q * dt * E[0]) / (2*m))
    velocity[0, 1] = v_min1[1]


    """Performing the boris mover simulation"""

    for k in range(K):
        half_acc = (q * dt * E[k]) / (2*m) #half acceleration stored as a temp variable
        v_min = np.array([velocity[k, 0] + half_acc, velocity[k, 1]]) #performing the half acceleration

        v_plus = np.matmul(rot_mat, v_min) #rotating

        velocity[k+1, 0] = v_plus[0] + half_acc #doing the second half acceleration in x-dir
        velocity[k+1, 1] = v_plus[1] #doing the second half acceleration in y-dir

        position[k+1, 0] = position[k, 0] + (velocity[k+1, 0] * dt) #updating x-pos
        position[k+1, 1] = position[k, 1] + (velocity[k+1, 1] * dt) #updatin y_pos

        E[k+1] = -position[k+1, 0] #updating the electric field to E(x) = -x

    plt.plot(position[:, 0], position[:, 1], label = "linear field")

def sinusoidal_field(pos_0, v_0):
    """ Defining values """
    #creating empty arrays to fill with position and velocity
    position = np.zeros((K+1, 2))  
    velocity = np.zeros((K+1, 2))

    #defining initial values
    position[0] = np.array(pos_0) 
    velocity[0] = np.array(v_0)

    #defining electric and magnetic fields
    E = np.zeros((K+1)) #defining only E(x)
    B = 0 #defining B=0 for this task

    #defining E(x) at t=0 (to E(x) = -sin(x))
    E[0] = -np.sin(position[0,0])

    #defining theta 
    theta = - ((q * B * dt) / m)


    """Performing the half rotation backwards"""
    #defining the rotational matrix for the half rotation backwards
    theta_back = rotation(- (theta / 2))

    #defining the rotational matrix to be used in the for-loop
    rot_mat = rotation(theta)

    #performing the ACTUAL half rotation backwards
    v_min1 = np.matmul(theta_back, velocity[0])

    #performing the half deceleration
    velocity[0, 0] = v_min1[0] - ((q * dt * E[0]) / (2*m))
    velocity[0, 1] = v_min1[1]


    """Boris mover algorithm"""

    for k in range(K):
        half_acc = (q * dt * E[k]) / (2*m) #half acceleration stored as a temp variable
        v_min = np.array([velocity[k, 0] + half_acc, velocity[k, 1]]) #performing the half acceleration

        v_plus = np.matmul(rot_mat, v_min) #rotating

        velocity[k+1, 0] = v_plus[0] + half_acc #doing the second half acceleration in x-dir
        velocity[k+1, 1] = v_plus[1] #doing the second half acceleration in y-dir

        position[k+1, 0] = position[k, 0] + (velocity[k+1, 0] * dt) #updating x-pos
        position[k+1, 1] = position[k, 1] + (velocity[k+1, 1] * dt) #updatin y_pos

        E[k+1] = -np.sin(position[k+1, 0]) #updating the electric field to E(x) = -x

    plt.plot(position[:, 0], position[:, 1], label = "sinusoidal field")

if __name__ == "__main__": 
    oppgave_a = linear_field(x_0, v_0)
    oppgave_b = sinusoidal_field(x_0, v_0)

    plt.title('Starting position: ({x}, {y}) Starting velocity: ({v_x}, {v_y})'
    .format(x = x_0[0], y = x_0[1], v_x = v_0[0], v_y = v_0[1]))
    plt.xlabel('x-position (m)')
    plt.ylabel('y-position (m)')
    plt.legend()
    plt.show()

