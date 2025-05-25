import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation, PillowWriter

# Parameter ruang
L = 10.0
N = 256  # Gunakan jumlah grid yang lebih besar untuk metode spektral
x = np.linspace(-L/2, L/2, N, endpoint=False)
dx = x[1] - x[0]

# Parameter waktu
T = 5.0
dt = 0.01
num_steps = int(T / dt)
t = np.linspace(0, T, num_steps)

# Nilai viskositas
nu_values = [1, 0.1, 0.01]

# Kondisi awal Gaussian
def gaussian_initial_condition(x):
    return np.exp(-x**2 / 2)

# Sistem ODE untuk metode spektral
def burgers_spectral(u, t, k, nu):
    u_hat = np.fft.fft(u)
    u_hat_x = 1j * k * u_hat
    u_hat_xx = -k**2 * u_hat
    u_x = np.fft.ifft(u_hat_x)
    u_xx = np.fft.ifft(u_hat_xx)
    u_t = -u * u_x + nu * u_xx
    return u_t.real

# Membuat animasi
def animate(i, all_solutions, lines, time_text):
    for line, solutions in zip(lines, all_solutions):
        line.set_ydata(solutions[:, i])  # Update solusi untuk setiap nilai nu
    time_text.set_text(f'Waktu = {t[i]:.2f} s')  # Update anotasi waktu
    return lines + [time_text]

if __name__ == "__main__":
    # Diskritisasi bilangan gelombang
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)

    # Simpan semua solusi untuk variasi nu
    all_solutions = []
    for nu in nu_values:
        u_initial = gaussian_initial_condition(x)
        solutions = odeint(burgers_spectral, u_initial, t, args=(k, nu)).T
        all_solutions.append(solutions)

    # Setup animasi
    fig, ax = plt.subplots()
    colors = ['red', 'green', 'blue']
    labels = [f'ν = {nu}' for nu in nu_values]
    lines = []

    for color, label in zip(colors, labels):
        line, = ax.plot(x, all_solutions[0][:, 0], color=color, label=label)  # Inisialisasi garis
        lines.append(line)

    ax.set_xlim(-L/2, L/2)
    ax.set_ylim(-0.5, 1.5)  # Disesuaikan untuk semua solusi
    ax.set_xlabel('x')
    ax.set_ylabel('u')
    ax.set_title('Persamaan Burgers Metode Spectral dengan Variasi ν (Intial Gaussian)')
    ax.legend()
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))  # Anotasi waktu

    ani = FuncAnimation(fig, animate, fargs=(all_solutions, lines, time_text), frames=num_steps, interval=50, blit=True)
    ani.save('Burgers_Spectral_Variasi_nu.gif', writer=PillowWriter(fps=20))
    plt.show()