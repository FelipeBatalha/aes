# echo -n "abcdef" | openssl enc -e -a -aes-256-cbc -pass pass:YourPassword
import base64
import numpy as np


def string_to_binary(string):
    binary_string = ''
    binary_bytes = bytes(string, 'utf-8')
    for byte in binary_bytes:
        binary = bin(byte)[2:]  # indice ignora o 0b no inicio
        # faz um pad na esquerda se precisar para garantir 8 bits
        binary_string += binary.zfill(8)
    print(binary_string)
    return binary_string

# correct


def shift_rows():
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
        [0x49, 0x45, 0x7f, 0xC3],
        [0xDB, 0x39, 0x02, 0xC9],
        [0x87, 0x53, 0xd2, 0x6E],
        [0x3B, 0x89, 0xf1, 0xFF]
    ], dtype=np.uint16)

    row = mix_columns_matrix[2, :] * matrix[:, 2]
    x = None
    for i in range(4):
        if mix_columns_matrix[2][i] == 2:
            row[i] = matrix[i][2] << 1
            if row[i] > 0xFF:
                row[i] ^= 0x11B
        elif mix_columns_matrix[2][i] == 3:
            a = matrix[i][2] << 1
            if a > 0xFF:
                a ^= 0x11B
            b = matrix[i][2]
            row[i] = a ^ b

    print(hex(row[0] ^ row[1] ^ row[2] ^ row[3]))

    result = np.zeros((4, 4), dtype=np.uint8)

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
    mix_columns()

    '''
    a = string_to_binary('abcdef')
    b = string_to_binary('dsfsdf')
    xored = xor(a,b)
    binary_to_string(xored)


    binary_to_string('0101010001101000011001010010000001110001011101010110100101100011011010110010000001100010011100100110111101110111011011100010000001100110011011110111100000100000011010100111010101101101011100000111001100100000011011110111011001100101011100100010000000110001001100110010000001101100011000010111101001111001001000000110010001101111011001110111001100101110')
    print(base64.b64decode('VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIDEzIGxhenkgZG9ncy4='))
    '''
