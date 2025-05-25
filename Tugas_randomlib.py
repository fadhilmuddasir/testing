# Tugas Mandiri - Random Library
# Nama: Fadhil Muddasir
# NIM: 24723301

import secrets

#Getting systemRandom class instance out of secrets module
secretsGenerator = secrets.SystemRandom()

print("Generating 6 digit random OTP")
otp = secretsGenerator.randrange(100000, 999999)

print("Secure random OTP is ", otp)