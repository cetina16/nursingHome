from passlib.hash import pbkdf2_sha256 as hasher
password = "doctor1"
hashed = hasher.hash(password)
print(hashed)