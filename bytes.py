import base64
import numpy as np
from sbox import sub_bytes
from expansion import key_expansion

def add_round_key(state, key):
    return state ^ key

def string_to_hex(string):
    array = np.zeros(16, dtype=np.uint8)
    binary_bytes = bytes(string, 'utf-8')
    i = 0
    for byte in binary_bytes:
        array[i] = byte
        i += 1
    array = np.reshape(array,(4,4))
    return array

def shift_rows(state):
    state[1, :] = np.roll(state[1, :], -1)
    state[2, :] = np.roll(state[2, :], -2)
    state[3, :] = np.roll(state[3, :], -3)
    return state

def mix_columns(state):
    mix_columns_matrix = np.array([
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ], dtype=np.uint16)

    result = np.zeros((4, 4), dtype=np.uint8)

    for row in range(4):
        for col in range(4):
            product = mix_columns_matrix[row, :] * state[:, col]
            for i in range(4):
                if mix_columns_matrix[row][i] == 2:
                    product[i] = state[i][col] << 1
                    if product[i] > 0xFF:
                        product[i] ^= 0x11B
                elif mix_columns_matrix[row][i] == 3:
                    a = state[i][col] << 1
                    if a > 0xFF:
                        a ^= 0x11B
                    b = state[i][col]
                    product[i] = a ^ b

            result[row][col] = product[0] ^ product[1] ^ product[2] ^ product[3]

    return result.astype(np.uint8)


def hex_to_string(hexadecimal):
    string = ''
    hexadecimal = hexadecimal.flatten()
    for byte in hexadecimal:
        string += str(hex(byte)[2:].zfill(2))
    #gota change the format later
    print(string)
    string = bytes.fromhex(string)
    string = base64.b64encode(string).decode('utf-8')
    return string


def xor(binary1, binary2):
    xored = ''
    if len(binary1) != len(binary2):
        raise ValueError("Xor between different size strings wont happen")
    for a, b in zip(binary1, binary2):
        xored += str(int(a) ^ int(b))
    print(xored)
    return xored


def aes_encryption(rounds, state, key):


    np.set_printoptions(formatter={'int': hex})

    #state = string_to_hex(state)
    #print(hex_to_string(state))
    print(f'Message:\n {state}')

    #key = string_to_hex(key)
    #print(hex_to_string(key))
    print(f'Key:\n {key}')

    print('Key Expansion:')
    keys = key_expansion(key, rounds)

    state = add_round_key(state,key)
    print('AddRoundKey:')
    print(state)

    for round in range(1,rounds+1):
        print(f"Round {round}")
        state = sub_bytes(state)
        #print('SubBytes:')
        #print(state)
        state = shift_rows(state)
        #print('ShiftRows:')
        #print(state)
        if round < rounds:
            print('MixColumns:')
            state = mix_columns(state)
            print(state)
        state = add_round_key(state,keys[round])
        print('AddRoundKey:')
    print(state)
    print(f'Result : {hex_to_string(state)}')


if __name__ == "__main__":
  

    key = np.array([
        [0x2b, 0x28, 0xab, 0x09],
        [0x7e, 0xae, 0xf7, 0xcf],
        [0x15, 0xd2, 0x15, 0x4f],
        [0x16, 0xa6, 0x88, 0x3c]
    ], dtype=np.uint8)

    state = np.array([
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34]
    ], dtype=np.uint16)

    '''state = np.array([
        [0x6b, 0xc1, 0xbe, 0xe2],
        [0x2e, 0x40, 0x9f, 0x96],
        [0xe9, 0x3d, 0x7e, 0x11],
        [0x73, 0x93, 0x17, 0x2a]
    ], dtype=np.uint16)
    #6bc1bee22e409f96e93d7e117393172a

    key = np.array([
            [0x2b, 0x7e, 0x15, 0x16],
            [0x28, 0xae, 0xd2, 0xa6],
            [0xab, 0xf7, 0x15, 0x88],
            [0x09, 0xcf, 0x4f, 0x3c]
        ], dtype=np.uint16)
    #2b7e151628aed2a6abf7158809cf4f3c'''
    
    rounds = 10
    aes_encryption(rounds, state,key)