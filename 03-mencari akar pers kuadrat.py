import math

# Fungsi untuk mencari akar persamaan kuadrat
def find_roots(a, b, c):
    # Hitung diskriminan
    D = b**2 - 4*a*c
    
    # Gunakan if-else untuk menentukan jenis akar
    if D > 0:
        root1 = (-b + math.sqrt(D)) / (2*a)
        root2 = (-b - math.sqrt(D)) / (2*a)
        return f"Dua akar nyata: {root1} dan {root2}"
    elif D == 0:
        root = -b / (2*a)
        return f"Satu akar nyata (akar kembar): {root}"
    else:
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(-D) / (2*a)
        return f"Dua akar imajiner: {real_part} + {imaginary_part}i dan {real_part} - {imaginary_part}i"

# Contoh penggunaan
a = 1
b = -3
c = 2

result = find_roots(a, b, c)
print(result)

a = 1
b = 2
c = 1

result = find_roots(a, b, c)
print(result)

a = 1
b = 1
c = 1

result = find_roots(a, b, c)
print(result)