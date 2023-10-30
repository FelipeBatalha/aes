import numpy as np
from encrypt import string_to_hex, aes_encryption

input_file = 'ah-pronto.png'
output_file = 'encrypted.bin'


def encrypt(rounds):
    iv = b"myKingBu"
    key = string_to_hex("Thats my Kung Fu").transpose()
    with open(input_file, 'rb') as file_in, open(output_file, 'wb') as file_out:
        counter = 0
        file_out.write(iv)
        while True:
            print(counter)
            data = file_in.read(16)
            if len(data) == 0:
                break

            nonce = iv + counter.to_bytes(8, byteorder='big')  # Create the unique nonce
            keystream = aes_encryption(rounds, string_to_hex(nonce).transpose(), key)
            ciphertext = bytes(x ^ y for x, y in zip(keystream, data))
            file_out.write(ciphertext)
            counter += 1

def decrypt(rounds):
    key = string_to_hex("Thats my Kung Fu").transpose()
    with open('encrypted.bin', 'rb') as file_in, open('decrypted.png', 'wb') as file_out:
        counter = 0
        iv = file_in.read(8)
        print(iv)
        while True:
            data = file_in.read(16)
            if len(data) == 0:
                break
            print(counter)

            nonce = iv + counter.to_bytes(8, byteorder='big')
            keystream = aes_encryption(rounds, string_to_hex(nonce).transpose(), key)
            plaintext = bytes(x ^ y for x, y in zip(keystream,data))
            file_out.write(plaintext)
            counter += 1

if __name__ == "__main__":
     
    while True:
        print("Escolha uma opção:")
        print("1. Cifrar")
        print("2. Decifrar")
        print("3. Sair")

        choice = input("Escolha: ")

        if choice == "1":
            rounds = int(input("Número de rounds: "))
            encrypt(rounds)
        elif choice == "2":
            rounds = int(input("Número de rounds: "))
            decrypt(rounds)
        elif choice == "3":
            break
        else:
            print("Escolha inválida. Selecione 1, 2, or 3.")
