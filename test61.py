from pwn import *
import re

host = "verbal-sleep.picoctf.net"
port = 49406

# Connect to the remote server
conn = remote(host, port)

# Step 1: Receive the introduction and extract the secret cheese
intro = conn.recvuntil(b"What would you like to do?").decode()
print(intro)

# Extract the secret cheese from the intro message using regex
secret_cheese = re.search(r"secret cheese.*?:\s*([A-Z]+)", intro).group(1)
print(f"Secret Cheese: {secret_cheese}")

# Step 2: Choose the encrypt option and wait for the encryption prompt
conn.sendline(b'e')
prompt = conn.recvuntil(b"encrypt?").decode()
print(prompt)

# Send the known cheese string "CHEDDAR" to get its encrypted version
known_cheese = "CHEDDAR"
conn.sendline(known_cheese.encode())

# Receive and print the encrypted version of "CHEDDAR"
encrypted_cheddar_line = conn.recvline().decode()
print(f"Encrypted line received: {encrypted_cheddar_line.strip()}")

# Extract the encrypted cheese part from the response
encrypted_cheddar = encrypted_cheddar_line.strip().split(": ")[1]

# Determine the Caesar cipher shift by comparing the first letters of encrypted "CHEDDAR" and "CHEDDAR"
shift = (ord(encrypted_cheddar[0]) - ord(known_cheese[0])) % 26
print(f"Detected shift: {shift}")

# Step 3: Define a function to decode using the Caesar cipher
def decode_caesar(cipher, shift):
    return ''.join([chr((ord(c) - shift - 65) % 26 + 65) for c in cipher])

# Decode the secret cheese using the detected shift
decoded_cheese = decode_caesar(secret_cheese, shift)
print(f"Decoded Cheese: {decoded_cheese}")

# Wait for the prompt to guess the cheese
prompt2 = conn.recvuntil(b"What would you like to do?").decode()
print(prompt2)

# Send the command to guess the cheese
conn.sendline(b'g')

prompt3 = conn.recvuntil(b"cheese?").decode()
print(prompt3)

# Send the decoded cheese back to the server
conn.sendline(decoded_cheese.encode())

# Final Step: Receive and print the final response (likely containing the flag)
flag_response = conn.recvall(timeout=2).decode()
print(flag_response)

conn.close()
