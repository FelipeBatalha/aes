from encrypt import string_to_hex, aes_encryption
import os, sys


def encrypt(rounds,input,output):
    iv = b"myKingBu"
    key = string_to_hex("Thats my Kung Fu")
    size = os.path.getsize(input_file)
    with open(input, 'rb') as file_in, open(output, 'wb') as file_out:
        counter = 0
        encrypted_data = bytearray()
        while True:
            print(f"Cifrando: {(((counter * 16)/size) * 100):.2f}%")
            data = file_in.read(16)
            if len(data) == 0:
                break

            nonce = iv + counter.to_bytes(8, byteorder='big')  # Create the unique nonce
            keystream = aes_encryption(rounds, string_to_hex(nonce), key)
            ciphertext = bytes(x ^ y for x, y in zip(keystream, data))
            encrypted_data += ciphertext
            counter += 1
        file_out.write(encrypted_data)   

def decrypt(rounds,input,output):
    key = string_to_hex("Thats my Kung Fu")
    size = os.path.getsize(input_file)
    with open(input, 'rb') as file_in, open(output, 'wb') as file_out:
        counter = 0
        #iv = file_in.read(8)
        iv = b"myKingBu"
        #print(iv)
        while True:
            data = file_in.read(16)
            print(f"Decifrando: {(((counter * 16)/size) * 100):.2f}%")
            if len(data) == 0:
                break
            print(counter)

            nonce = iv + counter.to_bytes(8, byteorder='big')
            keystream = aes_encryption(rounds, string_to_hex(nonce), key)
            plaintext = bytes(x ^ y for x, y in zip(keystream,data))
            file_out.write(plaintext)
            counter += 1

if __name__ == "__main__":

    if len(sys.argv) != 4:
                    print("Uso: \nPara cifrar: python3 ctr-mode.py cifrar arquivo_de_entrada arquivo_de_saida\nPara decifrar: python3 ctr-mode.py decifrar arquivo_de_entrada arquivo_de_saida")
                    sys.exit(1)
    choice = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    while True:
        rounds = int(input("Número de rounds: "))

        if choice == "cifrar":           
            encrypt(rounds, input_file, output_file)
        elif choice == "decifrar":
            decrypt(rounds, input_file, output_file)
        elif choice == "3":
            break
        else:
            print("Escolha inválida. Digite cifrar ou decifrar, mais o nome dos arquivos de entrada e saida")
            break
        break
