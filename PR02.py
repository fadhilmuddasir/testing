# Menentukan fase air berdasarkan suhu dalam derajat Celcius
# Nama: Fadhil Muddasir
# NIM: 24723301

"""
Program ini akan menentukan fase air berdasarkan suhu dalam derajat Celcius
Berikut adalah Psuedo code dari program ini:
1. Mulai
2. Input suhu dalam derajat Celcius
3. Jika suhu < 0, cetak "Air dalam fase padat (es)"
4. Jika suhu >= 0 dan suhu < 100, cetak "Air dalam fase cair"
5. Jika suhu >= 100, cetak "Air dalam fase gas(uap)"
6. Selesai
"""
"""
Berikut adalah flowchart dari program ini:
Start
  |
  v
Input suhu
  |
  v
suhu < 0 ?
 /   \
Yes   No
/      \
|       suhu >=0 dan < 100 ?
|                /      \
|               Yes      No
|               /           \
|               |            |
|               v            v
Print:         Print:       Print:
"Air dalam     "Air dalam  "Air dalam
fase padat     fase         fase gas
(es)"          cair         (uap)"
|               |            |
v               v            v
End             End          End
"""
'''
# PROGRAM

while True:
    # Input suhu
    suhu = float(input("Masukkan suhu dalam derajat Celcius: "))

    # Syarat/Kondisi untuk menentukan fase air
    if suhu < 0:
        print("Air dalam fase padat (es)")
    elif suhu >= 0 and suhu < 100:
        print("Air dalam fase cair")
    else:
        print("Air dalam fase gas(uap)")

    # Opsi untuk melanjutkan atau mengakhiri program
    opsi = input("apakah anda ingin memasukkan suhu lagi? (y/n): ")
    if opsi.lower() != "y":
        print("Program selesai")
        break
'''

# NAMA : FADHIL MUDDASIR
# NIM : 24723301

def hitung_massa_jenis(massa, volume):
    """
    Fungsi untuk menghitung massa jenis benda.
    :massa: Massa benda dalam kilogram
    :volume: Volume benda dalam meter kubik
    :return: Massa jenis benda dalam kg/m^3
    """
    if massa <= 0:
        return "Massa tidak boleh negatif atau nol"
    elif volume <= 0:
        return "Volume tidak boleh negatif atau nol"
    else:
        massa_jenis = massa / volume
        return massa_jenis

def kondisi_benda(massa_jenis_benda, massa_jenis_cairan):
    """
    Fungsi untuk menentukan kondisi benda berdasarkan massa jenis benda dan massa jenis cairan.
    :massa_jenis_benda: Massa jenis benda dalam kg/m^3
    :massa_jenis_cairan: Massa jenis cairan dalam kg/m^3
    :return: Kondisi benda (mengapung, melayang, atau tenggelam)
    """
    if massa_jenis_benda < massa_jenis_cairan:
        return "Benda mengapung"
    elif massa_jenis_benda == massa_jenis_cairan:
        return "Benda melayang"
    else:
        return "Benda tenggelam"

# Massa jenis cairan dalam kg/m^3
massa_jenis_air = 1000
massa_jenis_minyak = 800
massa_jenis_air_garam = 1025  # Contoh tambahan untuk air garam

# Contoh penggunaan
massa = float(input("Masukkan massa benda dalam kilogram: "))
volume = float(input("Masukkan volume benda dalam meter kubik: "))
cairan = input("Pilih cairan (air/minyak/air garam): ").strip().lower()

massa_jenis_benda = hitung_massa_jenis(massa, volume)

if cairan == "air":
    massa_jenis_cairan = massa_jenis_air
elif cairan == "minyak":
    massa_jenis_cairan = massa_jenis_minyak
elif cairan == "air garam":
    massa_jenis_cairan = massa_jenis_air_garam
else:
    massa_jenis_cairan = None
    print("Cairan tidak dikenal")

if isinstance(massa_jenis_benda, str):
    print(massa_jenis_benda)
elif massa_jenis_cairan is not None:
    kondisi = kondisi_benda(massa_jenis_benda, massa_jenis_cairan)
    print(f"Massa jenis benda adalah {massa_jenis_benda} kg/m^3")
    print(f"Kondisi benda: {kondisi}")