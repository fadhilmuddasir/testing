import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  # Tambahkan import untuk menyimpan animasi sebagai GIF

# 1. Parameter umum
L = 10.0                      # Panjang domain
nx = 256                      # Jumlah grid points
x = np.linspace(-L/2, L/2, nx)  # Grid x
dx = x[1] - x[0]              # Jarak antar grid
dt = 0.01                     # Waktu infinitesimal
max_time = 5.0                # Waktu maksimum simulasi
nt = int(max_time / dt)       # Jumlah langkah waktu
nus = [1.0, 0.1, 0.01]        # Variasi viskositas

# 2. Kondisi awal Gaussian
def gaussian_initial_condition(x):
    return np.exp(-x**2 / 2)

# 3. Skema Finite Difference untuk persamaan Burgers
def solve_burgers_fd(u, nu, dt, dx, nt):
    solutions = [u.copy()]
    for _ in range(nt):
        u_old = u.copy()
        for i in range(1, nx - 1):
            # Skema Finite Difference
            convection = -u_old[i] * (u_old[i] - u_old[i - 1]) / dx
            diffusion = nu * (u_old[i + 1] - 2 * u_old[i] + u_old[i - 1]) / dx**2
            u[i] = u_old[i] + dt * (convection + diffusion)
        # Kondisi batas periodik
        u[0] = u[-2]
        u[-1] = u[1]
        solutions.append(u.copy())
    return np.array(solutions).T

# 4. Membuat animasi
def animate(i, all_solutions, lines, time_text):
    for line, solutions in zip(lines, all_solutions):
        line.set_ydata(solutions[:, i])  # Update solusi untuk setiap nilai nu
    time_text.set_text(f'Time: {i * dt:.2f} s')  # Update anotasi waktu
    return lines + [time_text]

if __name__ == "__main__":
    # Simpan semua solusi untuk variasi nu
    all_solutions = []
    for nu in nus:
        u_initial = gaussian_initial_condition(x)
        solutions = solve_burgers_fd(u_initial, nu, dt, dx, nt)
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
    ax.set_ylim(-0.5, 1.5)  # Disesuaikan untuk semua solusi
    ax.set_xlabel('x')
    ax.set_ylabel('u(x,t)')
    ax.set_title('Persamaan Burgers Metode FD dengan Variasi ν (Intial Gaussian)')
    ax.legend()
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    ani = FuncAnimation(fig, animate, fargs=(all_solutions, lines, time_text), frames=nt, interval=50, blit=True)

    # Simpan animasi sebagai GIF
    ani.save('Burgers_FD_Variasi_nu.gif', writer=PillowWriter(fps=20))
    plt.show()
