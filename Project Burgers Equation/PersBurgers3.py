# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Parameter umum
nx = 201              # Jumlah grid point
x = np.linspace(-6, 6, nx)  # Grid x
dx = x[1] - x[0]       # Jarak grid
nt = 2000              # Banyaknya langkah waktu
dt = 0.001             # Ukuran langkah waktu
nus = [1.0, 0.1, 0.01] # Variasi viskositas

# 2. Fungsi untuk solve Burgers' Equation dengan animasi
def burgers_animated(u, nu, nt, dt, dx):
    un = u.copy()
    for n in range(nt):
        u = (un 
             - un * dt / dx * (un - np.roll(un, 1)) 
             + nu * dt / dx**2 * (np.roll(un, -1) - 2*un + np.roll(un, 1)))
        un = u.copy()
        yield u  # Menghasilkan solusi pada setiap langkah waktu

# 3. Setup plot untuk animasi
fig, ax = plt.subplots(figsize=(10, 6))
lines = []
for nu, color in zip(nus, ['blue', 'green', 'red']):
    line, = ax.plot(x, np.zeros_like(x), color=color, label=f'ν = {nu}')
    lines.append(line)

ax.set_title('Evolusi Solusi Persamaan Burgers dengan Gaussian Initial Condition')
ax.set_xlabel('x')
ax.set_ylabel('u(x, t)')
ax.set_xlim(-6, 6)
ax.set_ylim(0, 1.1)
ax.legend()
ax.grid(True)

# 4. Fungsi update untuk animasi
def update(frame):
    for line, nu in zip(lines, nus):
        u0 = np.exp(-0.5 * x**2)  # Kondisi awal
        u_gen = burgers_animated(u0, nu, nt, dt, dx)  # Generator solusi
        u = next(u_gen) if frame < nt else u0  # Ambil solusi pada frame tertentu
        line.set_ydata(u)
    return lines

# 5. Buat animasi
ani = animation.FuncAnimation(fig, update, frames=nt, interval=30, blit=True)

# 6. Simpan animasi sebagai file .gif
ani.save('burgers_animation.gif', writer='pillow')

plt.show()
