import base64
import numpy as np
from sbox import undo_sub_bytes
from expansion import key_expansion
from encrypt import string_to_hex, hex_to_string, hex_string_to_array

def undo_add_round_key(state, key):
    return state ^ key


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

def aes_decryption(rounds, state, key):

    keys = key_expansion(key, rounds)

    keys.reverse()

    for round in range(0,rounds):
        state = undo_add_round_key(state,keys[round])
        if round > 0:
            state = undo_mix_columns(state)
        state = undo_shift_rows(state)
        state = undo_sub_bytes(state)
    state = undo_add_round_key(state,keys[-1])
    return hex_to_string(state.transpose())

if __name__ == "__main__":

    key = string_to_hex("Thats my Kung Fu")
    state = hex_string_to_array('29c3505f571420f6402299b31a02d73a')
    
    key = key.transpose()
    state = state.transpose()
    rounds = 10
    print(f'Texto decifrado: {aes_decryption(rounds, state,key).decode()}')