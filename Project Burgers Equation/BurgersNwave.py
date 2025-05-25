import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation, PillowWriter

# 1. Parameter umum
L = 12.0                      # Panjang domain
nx = 256                      # Jumlah grid points
x = np.linspace(-L/2, L/2, nx, endpoint=False)  # Grid x
dx = x[1] - x[0]              # Jarak antar grid
dt = 0.01                     # Waktu infinitesimal
max_time = 10.0               # Waktu maksimum simulasi
nt = int(max_time / dt)       # Jumlah langkah waktu
t = np.linspace(0, max_time, nt)  # Array waktu
nus = [1.0, 0.1, 0.01]        # Variasi viskositas

# 2. Kondisi awal N-wave
def n_wave_initial_condition(x):
    return np.exp(-0.5 * (x - 1)**2) - np.exp(-0.5 * (x + 1)**2)

# 3. Sistem ODE untuk metode spektral
def burgers_spectral(u, t, k, nu):
    u_hat = np.fft.fft(u)
    u_hat_x = 1j * k * u_hat
    u_hat_xx = -k**2 * u_hat
    u_x = np.fft.ifft(u_hat_x)
    u_xx = np.fft.ifft(u_hat_xx)
    u_t = -u * u_x + nu * u_xx
    return u_t.real

# 4. Membuat animasi
def animate(i, all_solutions, lines, time_text):
    for line, solutions in zip(lines, all_solutions):
        line.set_ydata(solutions[:, i])  # Update solusi untuk setiap nilai nu
    time_text.set_text(f'Waktu: {t[i]:.2f} detik')  # Update anotasi waktu
    return lines + [time_text]

if __name__ == "__main__":
    # Diskritisasi bilangan gelombang
    k = 2 * np.pi * np.fft.fftfreq(nx, d=dx)

    # Simpan semua solusi untuk variasi nu
    all_solutions = []
    for nu in nus:
        u_initial = n_wave_initial_condition(x)
        solutions = odeint(burgers_spectral, u_initial, t, args=(k, nu)).T
        all_solutions.append(solutions)

    # Setup animasi
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['red', 'green', 'blue']
    labels = [f'ν = {nu}' for nu in nus]
    lines = []

    for color, label in zip(colors, labels):
        line, = ax.plot(x, all_solutions[0][:, 0], color=color, label=label)  # Inisialisasi garis
        lines.append(line)

    ax.set_xlim(-L/2, L/2)
    ax.set_ylim(-1.5, 1.5)  # Disesuaikan untuk semua solusi
    ax.set_xlabel('x')
    ax.set_ylabel('u(x,t)')
    ax.set_title('Evolusi Persamaan Burgers (Kondisi Insial N-Wave )')
    ax.legend()
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    ani = FuncAnimation(fig, animate, fargs=(all_solutions, lines, time_text), frames=nt, interval=50, blit=True)
    ani.save('BurgersNWAVE_Spect.gif', writer=PillowWriter(fps=20))
    plt.show()
