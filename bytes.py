# echo -n "abcdef" | openssl enc -e -a -aes-256-cbc -pass pass:YourPassword
import base64
import numpy as np
from sbox import sub_bytes


def string_to_binary(string):
    binary_string = ''
    binary_bytes = bytes(string, 'utf-8')
    for byte in binary_bytes:
        binary = bin(byte)[2:]  # indice ignora o 0b no inicio
        # faz um pad na esquerda se precisar para garantir 8 bits
        binary_string += binary.zfill(8)
    print(binary_string)
    return binary_string


def shift_products():
    matrix = np.arange(1, 17).reshape((4, 4))
    matrix[1, :] = np.roll(matrix[1, :], -1)  # one to the left
    matrix[2, :] = np.roll(matrix[2, :], -2)  # two to the left
    matrix[3, :] = np.roll(matrix[3, :], -3)  # three to the left
    print(matrix)
    return matrix


def mix_columns():
    mix_columns_matrix = np.array([
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ], dtype=np.uint8)

    matrix = np.array([
        [0x49, 0x45, 0x7f, 0x77],
        [0xDB, 0x39, 0x02, 0xde],
        [0x87, 0x53, 0xd2, 0x96],
        [0x3B, 0x89, 0xf1, 0x1a]
    ], dtype=np.uint16)

    result = np.zeros((4, 4), dtype=np.uint8)

    for row in range(4):
        for col in range(4):
            product = mix_columns_matrix[row, :] * matrix[:, col]
            for i in range(4):
                if mix_columns_matrix[row][i] == 2:
                    product[i] = matrix[i][col] << 1
                    if product[i] > 0xFF:
                        product[i] ^= 0x11B
                elif mix_columns_matrix[row][i] == 3:
                    a = matrix[i][col] << 1
                    if a > 0xFF:
                        a ^= 0x11B
                    b = matrix[i][col]
                    product[i] = a ^ b

            result[row][col] = product[0] ^ product[1] ^ product[2] ^ product[3]

    np.set_printoptions(formatter={'int': hex})
    print(result)


def binary_to_string(binary):
    string = ''
    for byte in range(0, len(binary) - 1, 8):  # indice ignora o 0b no inicio
        x = binary[byte:byte+8]
        string += chr(int(x, 2))
    print(string)
    return string


def xor(binary1, binary2):
    xored = ''
    if len(binary1) != len(binary2):
        raise ValueError("Xor between different size strings wont happen")
    for a, b in zip(binary1, binary2):
        xored += str(int(a) ^ int(b))
    print(xored)
    return xored


if __name__ == "__main__":

    np.set_printoptions(formatter={'int': hex})
    
    state = np.array([
        [0xa4, 0x68, 0x6b, 0x02],
        [0x9c, 0x9f, 0x5b, 0x6a],
        [0x7f, 0x35, 0xea, 0x50],
        [0xf2, 0x2b, 0x43, 0x49]
    ], dtype=np.uint8)
    

    state = sub_bytes(state)
    state = mix_columns(state)

    '''
    a = string_to_binary('abcdef')
    b = string_to_binary('dsfsdf')
    xored = xor(a,b)
    binary_to_string(xored)


    binary_to_string('0101010001101000011001010010000001110001011101010110100101100011011010110010000001100010011100100110111101110111011011100010000001100110011011110111100000100000011010100111010101101101011100000111001100100000011011110111011001100101011100100010000000110001001100110010000001101100011000010111101001111001001000000110010001101111011001110111001100101110')
    print(base64.b64decode('VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIDEzIGxhenkgZG9ncy4='))
    '''
