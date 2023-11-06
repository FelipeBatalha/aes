from encrypt import string_to_hex, aes_encryption
import os
import sys


def encrypt(rounds, input, output, key, iv):
    size = os.path.getsize(input_file)
    with open(input, 'rb') as file_in, open(output, 'wb') as file_out:
        counter = 0
        encrypted_data = bytearray()
        while True:
            data = file_in.read(16)            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Cifrando: {(((counter * 16)/size) * 100):.2f}%")
            
            if len(data) == 0:
                break

            # Create the unique nonce
            nonce = iv + counter.to_bytes(8, byteorder='big')
            keystream = aes_encryption(rounds, string_to_hex(nonce), key)
            ciphertext = bytes(x ^ y for x, y in zip(keystream, data))
            encrypted_data += ciphertext
            counter += 1
        file_out.write(encrypted_data)


def decrypt(rounds, input, output, key, iv):
    size = os.path.getsize(input_file)
    with open(input, 'rb') as file_in, open(output, 'wb') as file_out:
        counter = 0
        while True:
            data = file_in.read(16)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Decifrando: {(((counter * 16)/size) * 100):.2f}%")
            if len(data) == 0:
                break

            nonce = iv + counter.to_bytes(8, byteorder='big')
            keystream = aes_encryption(rounds, string_to_hex(nonce), key)
            plaintext = bytes(x ^ y for x, y in zip(keystream, data))
            file_out.write(plaintext)
            counter += 1


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Uso: \nPara cifrar: python3 ctr-mode.py cifrar arquivo_de_entrada arquivo_de_saida chave iv \
            Para decifrar: python3 ctr-mode.py decifrar arquivo_de_entrada arquivo_de_saida chave iv")
        sys.exit(1)
    choice = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key = string_to_hex(sys.argv[4])
    iv = bytes(sys.argv[5], 'utf-8')

    while True:
        rounds = int(input("Número de rounds: "))

        if choice == "cifrar":
            encrypt(rounds, input_file, output_file, key, iv)
        elif choice == "decifrar":
            decrypt(rounds, input_file, output_file, key, iv)
        elif choice == "3":
            break
        else:
            print("Escolha inválida. Digite cifrar ou decifrar, mais o nome dos arquivos de entrada e saida")
            break
        print("Operação concluída.")
        break
