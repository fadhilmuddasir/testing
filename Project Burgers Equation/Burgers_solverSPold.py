""" 
This file was built to solve numerically 1D Burgers' equation wave equation with the FFT. The equation corresponds to :

$\dfrac{\partial u}{\partial t} + \mu u\dfrac{\partial u}{\partial x} = \nu \dfrac{\partial^2 u}{\partial x^2}$
 
where
 - u represent the signal
 - x represent the position
 - t represent the time
 - nu and mu are constants to balance the non-linear and diffusion terms.

Copyright - © SACHA BINDER - 2021
"""

############## MODULES IMPORTATION ###############
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


############## CUSTOM PLOTTING FUNCTIONS ###############

def plot_a_frame_1D(X, u, t, L_x, y_min, y_max, title):
    plt.figure()
    plt.plot(X, u, label=f't = {t:.2f}s')
    plt.xlim(0, L_x)
    plt.ylim(y_min, y_max)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('u')
    plt.legend()
    plt.grid()
    plt.show()

def anim_1D(X, U, dt, interval, repeat, xlim, ylim):
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel('x')
    ax.set_ylabel('u')

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        line.set_data(X, U[:, frame])
        return line,

    frames = U.shape[1]
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=interval, repeat=repeat)
    plt.show()
    return ani

def plot_spatio_temp_3D(X, T, U):
    from mpl_toolkits.mplot3d import Axes3D
    X, T = np.meshgrid(X, T)  # Fixed import issue by using numpy.meshgrid
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, T, U.T, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel('u')
    plt.show()

def plot_spatio_temp_flat(X, U, T):
    plt.figure()
    plt.imshow(U, extent=[X[0], X[-1], T[-1], T[0]], aspect='auto', cmap='viridis')
    plt.colorbar(label='u')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.title('Spatio-temporal evolution')
    plt.show()

def plot_sequence(X, U, T):
    plt.figure()
    for i in range(0, len(T), max(1, len(T) // 10)):
        plt.plot(X, U[i], label=f't = {T[i]:.2f}s')
    plt.xlabel('x')
    plt.ylabel('u')
    plt.legend()
    plt.grid()
    plt.title('Sequence of profiles')
    plt.show()


############## SET-UP THE PROBLEM ###############

mu = 1
nu = 0.01 #kinematic viscosity coefficient
    
#Spatial mesh
L_x = 10 #Range of the domain according to x [m]
dx = 0.01 #Infinitesimal distance
N_x = int(L_x/dx) #Points number of the spatial mesh
X = np.linspace(0,L_x,N_x) #Spatial array

#Temporal mesh
L_t = 8 #Duration of simulation [s]
dt = 0.025  #Infinitesimal time
N_t = int(L_t/dt) #Points number of the temporal mesh
T = np.linspace(0,L_t,N_t) #Temporal array

#Wave number discretization
k = 2*np.pi*np.fft.fftfreq(N_x, d = dx)


#Def of the initial condition    
u0 = np.exp(-(X-3)**2/2) #Single space variable fonction that represent the wave form at t = 0
# plot_a_frame_1D(X,u0,0,L_x,0,1.2,'Initial condition')

############## EQUATION SOLVING ###############

#Definition of ODE system (PDE ---(FFT)---> ODE system)
def burg_system(u,t,k,mu,nu):
    #Spatial derivative in the Fourier domain
    u_hat = np.fft.fft(u)
    u_hat_x = 1j*k*u_hat
    u_hat_xx = -k**2*u_hat
    
    #Switching in the spatial domain
    u_x = np.fft.ifft(u_hat_x)
    u_xx = np.fft.ifft(u_hat_xx)
    
    #ODE resolution
    u_t = -mu*u*u_x + nu*u_xx
    return u_t.real
    

#PDE resolution (ODE system resolution)
U = odeint(burg_system, u0, T, args=(k,mu,nu,), mxstep=5000).T



############## PLOT ###############

# Anim
anim = anim_1D(X, U, dt, 2, True, (0, L_x), (0, 1.2))

# Plots
plot_spatio_temp_3D(X, T, U)
plot_spatio_temp_flat(X, U.T, T)
plot_sequence(X, U.T, T)  # Fixed missing argument by passing T






