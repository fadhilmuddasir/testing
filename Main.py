
def print_increasing(n, i=0):
    if i < n:
        print(10**(3*i))
        print_increasing(n, i + 1)  # Panggilan rekursif

def print_decreasing(n):
    if n >= 0:
        print(10**(3*n))
        print_decreasing(n - 1)  # Panggilan rekursif

n = 1
print_increasing(n)
print_decreasing(n)
