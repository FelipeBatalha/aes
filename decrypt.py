import base64
import numpy as np
from sbox import undo_sub_bytes
from expansion import key_expansion

def undo_add_round_key(state, key):
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

def hex_string_to_array(string):
    print(len(string))
    array = np.zeros(16, dtype=np.uint16)
    j = 0
    for i in range(1, 32 ,2):
        array[j] = int(string[i-1:i+1],16)
        j += 1
    array = np.reshape(array,(4,4))
    np.set_printoptions(formatter={'int': hex})
    print(array)
    return array

def undo_shift_rows(state):
    state[1, :] = np.roll(state[1, :], 1)
    state[2, :] = np.roll(state[2, :], 2)
    state[3, :] = np.roll(state[3, :], 3)
    return state

def undo_mix_columns(state):
    inv_mix_columns_matrix = np.array([
        [0x0E, 0x0B, 0x0D, 0x09],
        [0x09, 0x0E, 0x0B, 0x0D],
        [0x0D, 0x09, 0x0E, 0x0B],
        [0x0B, 0x0D, 0x09, 0x0E]
    ], dtype=np.uint8)

    result = np.zeros((4, 4), dtype=np.uint8)

    for col in range(4):
        for row in range(4):
            product = 0
            for i in range(4):
                product ^= _multiply(inv_mix_columns_matrix[row][i], state[i][col])
            result[row][col] = product

    return result.astype(np.uint8)

def _multiply(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        is_high_bit_set = (a & 0x80) != 0
        a <<= 1
        if is_high_bit_set:
            a ^= 0x1B
        b >>= 1
    return result



def hex_to_string(hexadecimal):
    string = ''
    hexadecimal = hexadecimal.flatten()
    for byte in hexadecimal:
        string += str(hex(byte)[2:].zfill(2))
    #gota change the format later
    print(string)
    string = bytes.fromhex(string)
    #string = base64.b64encode(string).decode('utf-8')
    return string

def aes_decryption(rounds, state, key):


    np.set_printoptions(formatter={'int': hex})

    #state = string_to_hex(state)
    #print(hex_to_string(state))
    print(f'Message:\n {state}')

    #key = string_to_hex(key)
    #print(hex_to_string(key))
    print(f'Key:\n {key}')

    print('Key Expansion:')
    keys = key_expansion(key, rounds)

    keys.reverse()
    print(keys[0])
    print(state)

    for round in range(0,rounds):
        print(f"Round {round}")
        print('UndoAddRoundKey:')
        state = undo_add_round_key(state,keys[round])
        print(state)
        if round > 0:
            print('UndoMixColumns:')
            state = undo_mix_columns(state)
            print(state)

        print('UndoShiftRows:')    
        state = undo_shift_rows(state)
        print(state)

        print('UndoSubBytes:')
        state = undo_sub_bytes(state)
        print(state)
        
    
    #undo first add key
    state = undo_add_round_key(state,keys[-1])
    print('UndoAddRoundKey:')
    print(state)

    print(f'Result : {hex_to_string(state.transpose())}')
    return hex_to_string(state.transpose())

if __name__ == "__main__":

    np.set_printoptions(formatter={'int': hex})

    key = string_to_hex("Thats my Kung Fu")
    state = hex_string_to_array('29c3505f571420f6402299b31a02d73a')
    
    key = key.transpose()
    state = state.transpose()
    rounds = 10
    aes_decryption(rounds, state,key)