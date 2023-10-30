import numpy as np
from encrypt import string_to_hex, aes_encryption
from decrypt import aes_decryption

input_file = 'ah-pronto.png'
output_file = 'encrypted.bin'


def encrypt():
    iv = b"myKingBu"
    key = string_to_hex("Thats my Kung Fu").transpose()
    with open(input_file, 'rb') as file_in, open(output_file, 'wb') as file_out:
        counter = 0
        #file_out.write(bytes.fromhex('89504e470d0a1a0a0000'))
        file_out.write(iv)
        while True:
            print(counter)
            data = file_in.read(16)
            if len(data) == 0:
                break

            #data = string_to_hex(data).transpose()
            nonce = iv + counter.to_bytes(8, byteorder='big')  # Create the unique nonce
            keystream = aes_encryption(10, string_to_hex(nonce).transpose(), key)
            
            ciphertext = bytes(x ^ y for x, y in zip(keystream, data))

            file_out.write(ciphertext)
            counter += 1

def decrypt():
    #iv = b"myKingBu"
    key = string_to_hex("Thats my Kung Fu").transpose()
    with open('encrypted.bin', 'rb') as file_in, open('decrypted.png', 'wb') as file_out:
        counter = 0
        #file_in.read(10)
        iv = file_in.read(8)
        print(iv)
        while True:
            data = file_in.read(16)
            if len(data) == 0:
                break
            print(counter)

            nonce = iv + counter.to_bytes(8, byteorder='big')  # Create the unique nonce
            keystream = aes_encryption(10, string_to_hex(nonce).transpose(), key)
            #plaintext = aes_decryption(10, string_to_hex(keystream).transpose(), key)
            plaintext = bytes(x ^ y for x, y in zip(keystream,data))

            file_out.write(plaintext)
            counter += 1

if __name__ == "__main__":
     encrypt()
     decrypt()
