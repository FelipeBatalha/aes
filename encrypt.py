import base64
import numpy as np
from sbox import sub_bytes
from expansion import key_expansion

def add_round_key(state, key):
    return state ^ key

def string_to_hex(string):
    array = np.zeros(16, dtype=np.uint8)
    if type(string) != bytes:
        binary_bytes = bytes(string, 'utf-8')
    else:
        binary_bytes = string
    i = 0
    for byte in binary_bytes:
        array[i] = byte
        i += 1
    array = np.reshape(array,(4,4))
    return array

def hex_string_to_array(string):
    array = np.zeros(16, dtype=np.uint16)
    j = 0
    for i in range(1, 32 ,2):
        array[j] = int(string[i-1:i+1],16)
        j += 1
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
    string = bytes.fromhex(string)
    return string


def aes_encryption(rounds, state, key):

    keys = key_expansion(key, rounds)
    state = add_round_key(state,key)

    for round in range(1,rounds+1):
        state = sub_bytes(state)
        state = shift_rows(state)
        if round < rounds:
            state = mix_columns(state)
        state = add_round_key(state,keys[round])
    return hex_to_string(state.transpose())


if __name__ == "__main__":
  
    '''
    key = hex_string_to_array('2b7e151628aed2a6abf7158809cf4f3c').transpose()
    state = hex_string_to_array('ae2d8a571e03ac9c9eb76fac45af8e51').transpose()
    '''

    key = string_to_hex("Thats my Kung Fu")
    state = string_to_hex("Two One Nine Two")

    
    key = key.transpose()
    state = state.transpose()
    rounds = 10
    print(f'Cifra: {aes_encryption(rounds, state,key).hex()}')