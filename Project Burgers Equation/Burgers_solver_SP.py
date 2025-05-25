r""" 
File ini dibuat untuk menyelesaikan persamaan gelombang Burgers 1D secara numerik menggunakan FFT. Persamaan tersebut adalah:

$\dfrac{\partial u}{\partial t} + \mu u\dfrac{\partial u}{\partial x} = \nu \dfrac{\partial^2 u}{\partial x^2}$
 
dimana:
 - u merepresentasikan sinyal
 - x merepresentasikan posisi
 - t merepresentasikan waktu
 - nu dan mu adalah konstanta untuk menyeimbangkan komponen non-linear dan difusi.

Hak Cipta - © SACHA BINDER - 2021
"""

############## IMPORT MODUL ###############
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  # Untuk menyimpan animasi dalam format GIF

############## FUNGSI PLOTTING CUSTOM ###############

# Fungsi untuk memplot satu frame 1D
def plot_a_frame_1D(X, u, t, L_x, y_min, y_max, title):
    plt.figure()
    plt.plot(X, u, label=f't = {t:.2f}s')
    plt.xlim(0, L_x)  # Batas sumbu x
    plt.ylim(y_min, y_max)  # Batas sumbu y
    plt.title(title)  # Judul grafik
    plt.xlabel('x')  # Label sumbu x
    plt.ylabel('u')  # Label sumbu y
    plt.legend()
    plt.grid()
    plt.show()

# Fungsi untuk membuat animasi 1D
def anim_1D(X, U, dt, interval, repeat, xlim, ylim, save_path=None):
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)  # Garis untuk animasi
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))  # Anotasi waktu
    ax.set_xlim(xlim)  # Batas sumbu x
    ax.set_ylim(ylim)  # Batas sumbu y
    ax.set_xlabel('x')  # Label sumbu x
    ax.set_ylabel('u')  # Label sumbu y
    ax.set_title('Waveform u(x,t)')  # Judul grafik

    # Inisialisasi animasi
    def init():
        line.set_data([], [])
        time_text.set_text('')  # Reset anotasi waktu
        return line, time_text

    # Update frame animasi
    def update(frame):
        line.set_data(X, U[:, frame])
        time_text.set_text(f't = {frame * dt:.2f} s')  # Perbarui anotasi waktu
        return line, time_text

    frames = U.shape[1]  # Jumlah frame
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=interval, repeat=repeat)

    # Simpan animasi sebagai GIF jika path diberikan
    if save_path:
        writer = PillowWriter(fps=30)
        ani.save(save_path, writer=writer)
        print(f"Animasi disimpan sebagai {save_path}")

    plt.show()
    return ani

# Fungsi untuk menyimpan plot sebagai file gambar
def save_plot(fig, save_path):
    fig.savefig(save_path, dpi=300)
    print(f"Plot disimpan sebagai {save_path}")

# Fungsi untuk memplot evolusi spatio-temporal dalam 3D
def plot_spatio_temp_3D(X, T, U):
    from mpl_toolkits.mplot3d import Axes3D
    X, T = np.meshgrid(X, T)  # Membuat grid untuk X dan T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, T, U.T, cmap='viridis')  # Plot permukaan 3D
    ax.set_xlabel('x')  # Label sumbu x
    ax.set_ylabel('t')  # Label sumbu t
    ax.set_zlabel('u')  # Label sumbu u
    ax.set_title('Evolusi Spatio-Temporal 3D')  # Judul grafik
    plt.show()

# Fungsi untuk memplot evolusi spatio-temporal dalam bentuk datar
def plot_spatio_temp_flat(X, U, T):
    plt.figure()
    plt.imshow(U, extent=[X[0], X[-1], T[-1], T[0]], aspect='auto', cmap='viridis')  # Plot sebagai gambar
    plt.colorbar(label='u')  # Tambahkan colorbar
    plt.xlabel('x')  # Label sumbu x
    plt.ylabel('t')  # Label sumbu t
    plt.title('Evolusi Spatio-Temporal Datar')  # Judul grafik
    plt.show()

# Fungsi untuk memplot urutan profil u(x,t) pada waktu tertentu
def plot_sequence(X, U, T):
    plt.figure()
    for i in range(0, len(T), max(1, len(T) // 10)):  # Pilih beberapa frame untuk ditampilkan
        plt.plot(X, U[i], label=f't = {T[i]:.2f}s')
    plt.xlabel('x')  # Label sumbu x
    plt.ylabel('u')  # Label sumbu u
    plt.legend()
    plt.grid()
    plt.title('Urutan Profil Seiring Waktu')  # Judul grafik
    plt.show()

############## PENGATURAN MASALAH ###############

mu = 1  # Koefisien non-linearitas
nu = 0.01  # Koefisien viskositas kinematik
    
# Mesh spasial
L_x = 10  # Panjang domain dalam arah x [m]
dx = 0.01  # Jarak infinitesimal
N_x = int(L_x/dx)  # Jumlah titik dalam mesh spasial
X = np.linspace(0, L_x, N_x)  # Array spasial

# Mesh temporal
L_t = 8  # Durasi simulasi [s]
dt = 0.025  # Waktu infinitesimal
N_t = int(L_t/dt)  # Jumlah titik dalam mesh temporal
T = np.linspace(0, L_t, N_t)  # Array temporal

# Diskritisasi bilangan gelombang
k = 2 * np.pi * np.fft.fftfreq(N_x, d=dx)

# Definisi kondisi awal
u0 = np.exp(-(X-3)**2/2)  # Fungsi gelombang awal
# plot_a_frame_1D(X, u0, 0, L_x, 0, 1.2, 'Kondisi Awal')

############## PENYELESAIAN PERSAMAAN ###############

# Definisi sistem ODE (PDE ---(FFT)---> Sistem ODE)
def burg_system(u, t, k, mu, nu):
    # Turunan spasial dalam domain Fourier
    u_hat = np.fft.fft(u)
    u_hat_x = 1j * k * u_hat
    u_hat_xx = -k**2 * u_hat
    
    # Beralih ke domain spasial
    u_x = np.fft.ifft(u_hat_x)
    u_xx = np.fft.ifft(u_hat_xx)
    
    # Penyelesaian ODE
    u_t = -mu * u * u_x + nu * u_xx
    return u_t.real

# Penyelesaian PDE (penyelesaian sistem ODE)
U = odeint(burg_system, u0, T, args=(k, mu, nu), mxstep=5000).T

############## PLOTTING ###############

# Animasi
anim = anim_1D(X, U, dt, 2, True, (0, L_x), (0, 1.2), save_path="Burgersanimation_spectral.gif")  # Simpan animasi sebagai GIF

# Plot
plot_spatio_temp_3D(X, T, U)  
plot_spatio_temp_flat(X, U.T, T)  
plot_sequence(X, U.T, T)
