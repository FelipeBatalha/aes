import numpy as np
from encrypt import string_to_hex, aes_encryption
from decrypt import aes_decryption

input_file = 'ah-pronto.png'
output_file = 'encrypted.bin'


'''with open(input_file, 'rb') as file_in, open(output_file, 'wb') as file_out:
        i = 0
        key = string_to_hex("Thats my Kung Fu").transpose()
        while True:
            i += 1
            data = file_in.read(16)
            if len(data) == 0:
                break
            print(i)
            data = string_to_hex(data).transpose()
            data = aes_encryption(10,data,key)
            file_out.write(data)
            #file_out.write(bytes(data,'utf-8'))'''

with open('encrypted.bin', 'rb') as file_in, open('decrypted.png', 'wb') as file_out:
        i = 0
        key = string_to_hex("Thats my Kung Fu").transpose()
        while True:
            i += 1
            data = file_in.read(16)
            if len(data) == 0:
                break
            print(i)
            data = string_to_hex(data).transpose()
            data = aes_decryption(10,data,key)
            file_out.write(data)
            #file_out.write(bytes(data,'utf-8'))
