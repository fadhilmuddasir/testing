import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter  # berguna untuk skala `logit`

# Memperbaiki state acak untuk reproduktifitas
np.random.seed(19680801)

# Membuat data dalam interval ]0, 1[
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

# Membuat figure 1
plt.figure(1)

# Linear
plt.subplot(221)
plt.plot(x, y)
plt.yscale('linear')
plt.title('linear')
plt.grid(True)

# Log
plt.subplot(222)
plt.plot(x, y)
plt.yscale('log')
plt.title('log')
plt.grid(True)

# Symmetric log
plt.subplot(223)
plt.plot(x, y - y.mean())
plt.yscale('symlog', linthresh=0.01)
plt.title('symlog')
plt.grid(True)

# Logit
plt.subplot(224)
plt.plot(x, y)
plt.yscale('logit')
plt.title('logit')
plt.grid(True)

# Format label minor tick dari sumbu y menjadi string kosong dengan `NullFormatter`,
# untuk menghindari terlalu banyak label pada sumbu.
plt.gca().yaxis.set_minor_formatter(NullFormatter())

# Sesuaikan tata letak subplot, karena skala logit mungkin memerlukan lebih banyak ruang
# dari biasanya, karena label y-tick seperti "1-10^{-3}"
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)

# Menampilkan grafik
plt.show()