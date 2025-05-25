import numpy  # Memberikan ekspresi matematika atau matriks
import sympy  # SymPy adalah pustaka matematika simbolik untuk Python

from sympy import init_printing       
init_printing(use_latex=True)  # Output menggunakan LATEX.

lineSingle = '------------------------------------------------'

print("Menyelesaikan Persamaan Burgers 1D menggunakan Metode Finite Difference")
print("Konveksi: Skema Backward Difference")
print("Difusi: Skema Central Difference\n")

# Inisialisasi variabel simbolik untuk kondisi awal
x, nu, t = sympy.symbols('x nu t')
phi = (sympy.exp(-(x - 4*t)**2/(4*nu*(t + 1))) + sympy.exp(-(x - 4*t - 2*sympy.pi)**2/(4*nu*(t+1))))  # Ekspresi phi

print(lineSingle)
print("Mencetak ekspresi phi")
print(lineSingle)
print(phi)


phiprime = phi.diff(x)  # Turunan terhadap x
phiprime

from sympy.utilities.lambdify import lambdify  # Mengubah ekspresi simbolik menjadi fungsi Python

u = -2*nu*(phiprime/phi) + 4  # Ekspresi kondisi awal

print(lineSingle)
print("Ekspresi Kondisi Awal")
print(lineSingle)
print(u)

ufunc = lambdify((t, x, nu), u)  # Membuat fungsi Python dari ekspresi simbolik


from matplotlib import pyplot     

# Mengatur grid

nx = 101                                # Jumlah titik grid
nt = 20                                 # Jumlah langkah waktu
dx = 2 * numpy.pi / (nx - 1)            # Jarak antar grid
nu = .07                                # Viskositas
dt = dx * nu                            # Ukuran langkah waktu

x = numpy.linspace(0, 2 * numpy.pi, nx)
un = numpy.empty(nx)
t = 0                                   # Waktu awal t = 0

u = numpy.asarray([ufunc(t, x0, nu) for x0 in x])  # Kondisi awal menggunakan fungsi lambdify

print(lineSingle)
print("Menghitung Solusi Awal")
print(lineSingle)
print(u)

# Menghitung solusi analitik
print(lineSingle)
print("Menghitung Solusi Analitik")
print(lineSingle)

u_analytical = numpy.asarray([ufunc(nt * dt, xi, nu) for xi in x])  # Solusi analitik

print(lineSingle)
print("Mencetak Solusi Analitik")
print(lineSingle)

print(u_analytical)

# Menghitung solusi numerik
print(lineSingle)
print("Menghitung Solusi Numerik...")
print(lineSingle)

for n in range(nt):  # Iterasi waktu
    un = u.copy()
    for i in range(1, nx - 1):  # Iterasi ruang

        # Backward Difference untuk Konveksi
        # Central Difference untuk Difusi
        
        u[i] = un[i] - un[i]*dt/dx*(un[i] - un[i-1]) + nu*dt/dx**2*(un[i+1]-2*un[i]+un[i-1])

    # Kondisi batas periodik
    
    u[0] = un[0] - un[0]*dt/dx*(un[0] - un[-2]) + nu*dt/dx**2*(un[1]-2*un[0]+un[-2])
    u[-1] = u[0]

print(lineSingle)
print("Mencetak Solusi Numerik")
print(lineSingle)

print(u)


# Menggabungkan semua hasil dalam satu grafik
print(lineSingle)
print("Memplot Kondisi Awal, Solusi Analitik, dan Solusi Numerik")
print(lineSingle)

pyplot.figure(figsize=(11, 7), dpi=100)

# Plot kondisi awal
pyplot.plot(x, numpy.asarray([ufunc(0, xi, nu) for xi in x]), marker='o', lw=2, label='Kondisi Awal')

# Plot solusi analitik
pyplot.plot(x, u_analytical, label='Solusi Analitik')

# Plot solusi numerik
pyplot.plot(x, u, marker='x', lw=2, label='Solusi Numerik')

pyplot.xlim([0, 2 * numpy.pi])
pyplot.ylim([0, 10])

pyplot.title('Persamaan Burgers 1D: Kondisi Awal, Solusi Analitik, dan Solusi Numerik')
pyplot.xlabel('Ruang Grid')
pyplot.ylabel('Kecepatan')

pyplot.legend()
pyplot.grid()
pyplot.show()