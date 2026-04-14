""" Module 04 Midterm: Build a secure data transmission app with hashing and encryption."""


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib
import secrets


def get_hash(data):
    """Generates a SHA-256 hash in order to verify the integrity of the message."""
    return hashlib.sha256(data).hexdigest()

def encrypt_data(plaintext, key):
    """Encrypts plaintext with AES and padding."""
    # Secrets is a built in python library that may still use os.urandom() but will hopefully provides enough entropy for the purposes of this exam. 
    init_vector = secrets.token_bytes(16)

    pad = padding.PKCS7(128).padder()
    padded_data = pad.update(plaintext.encode()) + pad.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(init_vector), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return init_vector, ciphertext

def decrypt_data(init_vector, ciphertext, key):
    """Decrypts ciphertext and removes padding."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(init_vector), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpad = padding.PKCS7(128).unpadder()
    plaintext_bytes = unpad.update(padded_data) + unpad.finalize()
    return plaintext_bytes.decode()


# Requests user input.
user_message = input(f'\nEnter a message for secured transfer:\n')

# Generate a 256 bit secure key using the secrets module
shared_key = secrets.token_bytes(32)

# Use the hash function to hash the input for integrity validation.
original_hash = get_hash(user_message.encode())
print(f'\n[+] Original SHA-256 Hash: {original_hash}')

# Encrypt the input
init_vector, ciphertext = encrypt_data(user_message, shared_key)

print(f'[+] Encrypted Message: {ciphertext.hex()}')
print(f'[+] Initialization Vector: {init_vector.hex()}')

# Decrypt the message.
decrypted_message = decrypt_data(init_vector, ciphertext, shared_key)
print(f'[+] Decrypted Message: {decrypted_message}')

# Verify hash integrity
decrypted_hash = get_hash(decrypted_message.encode())
print(f'[+] Decrypted Hash: {decrypted_hash}')

if secrets.compare_digest(original_hash, decrypted_hash):
    print(f'\nIntegrity Verified: The hashes match.')
else:
    print(f'\nIntegrity Check Failed: Potential tampering detected.')