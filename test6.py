from pwn import *

# Connect to the server
host = "verbal-sleep.picoctf.net"
port = 49406

conn = remote(host, port)

# Receive initial data from server
response = conn.recv().decode()
print(response)

# Decrypt the secret cheese password
# Assuming the password needs simple decoding (ROT13/Base64/Hex)
# You might need to adapt this based on actual challenge details

def decrypt_cheese(encoded_password):
    try:
        # Hex decoding
        return bytes.fromhex(encoded_password).decode('utf-8')
    except:
        pass
    try:
        # Base64 decoding
        import base64
        return base64.b64decode(encoded_password).decode('utf-8')
    except:
        pass
    # ROT13 decoding
    import codecs
    return codecs.decode(encoded_password, 'rot_13')

# Main interaction loop
while True:
    response = conn.recv().decode()
    print(response)
    if "password" in response.lower():
        encoded_password = response.strip().split(': ')[-1]
        decoded_password = decrypt_cheese(encoded_password)
        print(f"Decoded password: {decoded_password}")
        conn.sendline(decoded_password.encode())
    elif "picoCTF{" in response:
        print("Flag:", response)
        break

conn.close()