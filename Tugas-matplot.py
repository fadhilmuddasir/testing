# NAMA  : FADHIL MUDDASIR
# NIM   : 24723301
# TUGAS MATPLOTLIB
'''
# 1
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

# Definisikan fungsi x1
def x1(t):
    return 0.15*t**2 - 5*t + 25

# Definisikan fungsi x2
def x2(t):
    return t + 15

# Definisikan nilai t
t = np.arange(-16., 50., 0.01)

# Buat array untuk menyimpan data t, x1(t), dan x2(t)
data = np.column_stack((t, x1(t), x2(t)))
# Simpan data ke file .txt
np.savetxt("output_data.txt", data, fmt="%.2f", header="t\tx1(t)\tx2(t)", comments='')
print("Data telah disimpan ke file 'output_data.txt'")

# Membuat grafik
plt.plot(t, x1(t), 'b-', label=r'$x_1(t) = 0.15t^2 - 5t + 25$')
plt.plot(t, x2(t), 'r-', label=r'$x_2(t) = t + 10$')

# Menambahkan garis sumbu t dan x(t)
plt.axhline(0, color='black', linewidth=1, linestyle='-')  # Garis horizontal (sumbu t)
plt.axvline(0, color='black', linewidth=1, linestyle='-')  # Garis vertikal (sumbu x(t))

# Cari titik potong antar fungsi x1(t) dan x2(t)
coeff_x1x2 = [0.15, -6, 10]  # Koefisien dari x1(t) - x2(t) = 0
t_intersect = np.roots(coeff_x1x2)  # Nilai t di mana x1(t) = x2(t) / nilai akar persamaan
x_intersect = x1(t_intersect)  # Nilai x pada titik potong

# Cari titik potong x1(t) dengan sumbu t (x1(t) = 0)
coeff_x1 = [0.15, -5, 25]
t_x1_roots = np.roots(coeff_x1)

# Cari titik potong x2(t) dengan sumbu t (x2(t) = 0)
coeff_x2 = [1, 15]
t_x2_root = np.roots(coeff_x2)

# Cari titik potong dengan sumbu x(t) (t = 0)
x1_di_t0 = x1(0)
x2_di_t0 = x2(0)

# Cetak hasil
print("Titik potong antar fungsi:")
for t, x in zip(t_intersect, x_intersect):
    print(f"t = {t:.2f}, x = {x:.2f}")

print("\nTitik potong x1(t) dengan sumbu t:")
for t in t_x1_roots:
    print(f"t = {t:.2f}, x = 0")

print("\nTitik potong x2(t) dengan sumbu t:")
print(f"t = {t_x2_root[0]:.2f}, x = 0")

print("\nTitik potong dengan sumbu x(t):")
print(f"x1(t): t = 0, x = {x1_di_t0:.2f}")
print(f"x2(t): t = 0, x = {x2_di_t0:.2f}")

#-----Membuat Tabel dengan Pandas----#
# Data titik potong
data_tabel = {
    "Titik": ["A", "B"],
    "Waktu (t)": [1.74, 38.26],
    "Posisi (x)": [16.74, 53.26]
}
# Buat DataFrame pandas
df = pd.DataFrame(data_tabel)
# Cetak tabel
print("\nTabel Titik Potong:")
print(df)


# Menambahkan titik potong ke grafik
plt.scatter(t_intersect, x_intersect, color='purple', label='Titik potong antar fungsi')
plt.scatter(t_x1_roots, [0, 0], color='blue', label='Titik potong x1(t) dengan sumbu t')
plt.scatter(t_x2_root, [0], color='red', label='Titik potong x2(t) dengan sumbu t')
plt.scatter([0, 0], [x1_di_t0, x2_di_t0], color='green', label='Titik potong dengan sumbu x(t)')

# Menambahkan anotasi untuk titik potong
plt.annotate('Titik A', xy=(1.74, 16.74), xytext=(5, 40),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             fontsize=10, color='purple')

plt.annotate('Titik B', xy=(38.26, 53.26), xytext=(32, 73),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             fontsize=10, color='purple')

# Menambahkan label pada sumbu x dan y
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Grafik fungsi $x_1(t)$ dan $x_2(t)$')
plt.legend()
plt.grid(True)
plt.show()
'''
# NAMA  : FADHIL MUDDASIR
# NIM   : 24723301
# TUGAS MATPLOTLIB
# 2
import numpy as np
import matplotlib.pyplot as plt

# Definisi fungsi fx1
def fx1(x, a):
    return np.e**(-a*x)

# Definisi fungsi fx2
def fx2(x, a):
    return 1 / np.cosh(x - a)

# Definisi fungsi fx3
def fx3(x, a, b):
    return np.sin(a*x) + b

# Nilai x
x = np.linspace(0, 4*np.pi, 100)

# Nilai a dan b
a = 2
b = 1

# Membuat grafik
plt.figure(1, figsize=(10, 8))  # Menentukan ukuran figure

# Subplot 1
plt.subplot(221)
plt.plot(x, fx1(x, a), label=r'$f(x) = e^{-ax}$', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='-')  # Garis horizontal
plt.axvline(0, color='black', linewidth=0.8, linestyle='-')  # Garis vertikal
plt.title(r'Fungsi Eksponensial $f(x) = e^{-ax}$', fontsize=12)
plt.xlabel(r'$x$', fontsize=10)
plt.ylabel(r'$f(x)$', fontsize=10)
plt.legend()
plt.grid(True)

# Subplot 2
plt.subplot(222)
plt.plot(x, fx2(x, a), label=r'$f(x) = \text{sech}(x-a)$', color='green')
plt.axhline(0, color='black', linewidth=0.8, linestyle='-')  # Garis horizontal
plt.axvline(0, color='black', linewidth=0.8, linestyle='-')  # Garis vertikal
plt.title(r'Fungsi Secant Hyperbolic $f(x) = \text{sech}(x-a)$', fontsize=12)
plt.xlabel(r'$x$', fontsize=10)
plt.ylabel(r'$f(x)$', fontsize=10)
plt.legend()
plt.grid(True)

# Subplot 3
plt.subplot(212)
plt.plot(x, fx3(x, a, b), label=r'$f(x) = \sin(ax) + b$', color='red')
plt.axhline(0, color='black', linewidth=0.8, linestyle='-')  # Garis horizontal
plt.axvline(0, color='black', linewidth=0.8, linestyle='-')  # Garis vertikal
plt.title(r'Fungsi Sinusoidal $f(x) = \sin(ax) + b$', fontsize=12)
plt.xlabel(r'$x$', fontsize=10)
plt.ylabel(r'$f(x)$', fontsize=10)
plt.legend()
plt.grid(True)

# Menampilkan grafik
plt.tight_layout()  # Menyesuaikan tata letak agar tidak tumpang tindih
plt.show()
