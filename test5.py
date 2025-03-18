from Crypto.Util.number import long_to_bytes, inverse
from sympy import factorint
import socket

# Connect to remote service
host, port = "verbal-sleep.picoctf.net", 51624

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    # Receive data
    received_data = s.recv(4096).decode()
    print(received_data)

    # Parse received data for N, e, and ciphertext
    lines = received_data.strip().split('\n')
    N = int(lines[0].split(":")[1].strip())
    e = int(lines[1].split(":")[1].strip())
    ciphertext = int(lines[2].split(":")[1].strip())

    # Factorize N to get primes p and q
    factors = factorint(N)
    p, q = factors.keys()

    # Compute phi(N)
    phi = (p - 1) * (q - 1)

    # Compute private key exponent d
    d = inverse(e, phi)

    # Decrypt the ciphertext
    plaintext = pow(ciphertext, d, N)

    # Convert decrypted message to bytes
    decrypted_flag = long_to_bytes(plaintext)

    print("Decrypted Flag:", decrypted_flag.decode())