import math
import numpy as np
#creating a rotation matrix for a rotation in the x axis

def rot_x(deg):
    a = math.cos(math.radians(deg))
    b = math.sin(math.radians(deg))
    C = np.array([[1,0,0],[0,a,b],[0,-b,a]])
    return C

#rotation about the y axis
def rot_y(deg):
    a = math.cos(math.radians(deg))
    b = math.sin(math.radians(deg))
    C = np.array([[a,0,-b],[0,1,0],[b,0,a]])
    return C

#rotation about the z axis
def rot_z(deg):
    a = math.cos(math.radians(deg))
    b = math.sin(math.radians(deg))
    C = np.array([[a,b,0],[-b,a,0],[0,0,1]])
    return C

#rot_x(37)
def quat_to_mat(quat):
    n = quat[0]
    eps = quat[1:4]
    C = (2*(n**2)-1)*np.identity(3) + 2*np.outer(eps,eps) - 2*n*crux(eps)
    return C.T

def crux(vect):
    C = np.array([[0,-vect[2],vect[1]],
                  [vect[2],0,-vect[0]],
                  [-vect[1],vect[0],0]])
    return C

#returns the imaginary compenent as a 3x1 array and the real component
def to_quat(axis,ang):
    ang = math.radians(ang)
    imag = axis*math.sin(ang/2)
    real = math.cos(ang/2)
    quat_i = np.array([imag[0],imag[1],imag[2]])
    quat_r = real
    return quat_i, quat_r

def quat_rot(q_real, q_im, vect):
    im_t = q_real*vect + crux(vect)@-q_im
    real_t = - np.dot(vect, -q_im)

    v_new = q_real*im_t + real_t*q_im + crux(q_im)@im_t

    return v_new

axis = np.array([0,0,1])
ang = 90
quat_i, quat_r = to_quat(axis,ang)
vector = np.array([0,1,0])
print(quat_rot(quat_r,quat_i,vector))

def triad(body_1, body_2, earth_1, earth_2):
    big_s = earth_1 / np.linalg.norm(earth_1)
    little_s = body_1 / np.linalg.norm(body_1)
    big_m = (np.cross(earth_1,earth_2))/np.linalg.norm(np.cross(earth_1,earth_2))
    little_m = (np.cross(body_1,body_2))/np.linalg.norm(np.cross(body_1,body_2))
    #print(little_m)
    #print(big_m)
    #print(big_s)
    #print(big_m)
    #print(earth_1@earth_2)
    #print(earth_1)
    #print(earth_2)
    #print(little_s)
    big_s_Cro_big_m = np.cross(big_s,big_m)
    little_s_Cro_little_m = np.cross(little_s,little_m)
    #print(little_s)
    #print(little_m)
    #print(little_s_Cro_little_m)
    a = np.vstack([big_s,big_m,big_s_Cro_big_m])
    #print(a.T)
    b = np.vstack([little_s,little_m,little_s_Cro_little_m])
    #print(b.T)
    #print(a)
    #print(b)
    C = a.T@b
    return C

def dcm2quat(C):

    """
    From "A Survey on the Computation of Quaternions from Rotation Matrices" by Soheil and Federico
    """

    qi_sign = C[2,1] - C[1,2]
    qj_sign = C[0,2] - C[2,0]
    qk_sign = C[1,0] - C[0,1]

    real = .25*np.sqrt((C[0,0] + C[1,1] + C[2,2] + 1)**2 +
                       (C[2,1] - C[1,2])**2 +
                       (C[0,2] - C[2,0])**2 +
                       (C[1,0] - C[0,1])**2)

    qi = .25*np.sqrt((C[2,1] - C[1,2])**2 +
                     (C[0,0] - C[1,1] - C[2,2] + 1)**2 +
                     (C[1,0] + C[0,1])**2 +
                     (C[2,0] + C[0,2])**2)

    qj = .25*np.sqrt((C[0,2] - C[2,0])**2 +
                     (C[1,0] + C[0,1])**2 +
                     (C[1,1] - C[0,0] - C[2,2] + 1)**2 +
                     (C[2,1] + C[1,2])**2)

    qk = .25*np.sqrt((C[1,0] - C[0,1])**2 +
                     (C[2,0] + C[0,2])**2 +
                     (C[2,1] + C[1,2])**2 +
                     (C[2,2] - C[0,0] - C[1,1] + 1)**2)

    if qi_sign < 0:
        qi = -qi

    if qj_sign < 0:
        qj = -qj

    if qk_sign <0:
        qk = -qk

    return real, np.hstack([qi, qj, qk])


#e_1 = np.array([0.57735027,0.57735027,0.57735027])
##print(e_1)
#e_2 = np.array([0,-0.40613847,0.91381155])
#b_1 = np.array([0.11547005,0.57735027,0.80829038])
#b_2 = np.array([0.61597667,0.74458719,-0.25722103])
#C = triad(b_2,b_1,e_2,e_1)

#print(e_1@C)
#print(b_1)
#print(dcm2quat(C))







