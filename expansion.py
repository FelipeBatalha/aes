import numpy as np
from sbox import sub_bytes

def key_expansion(key):
    rounds = 1
    rcon = np.zeros(4, dtype=np.uint8)
    expanded_key = np.zeros((4, 4 * (rounds + 1)), dtype=np.uint8)  # Initialize the expanded key

    for current_round in range(rounds):
        rot_word = np.roll(key[:, 3], -1)
        np.set_printoptions(formatter={'int': hex})
        print(rot_word)
        sub_word = sub_bytes(rot_word)
        print(sub_word)
        if current_round == 0:
            rcon[0] = 0x01
        else:
            rcon[0] = 2 * rcon[0]
            if rcon[0] >= 0x80:
                rcon[0] ^= 0x11b

        # XOR the key with rcon
        expanded_key[:, 0] = rcon ^ sub_word
        print(expanded_key[:, 0])

        begin = True
        for i in range(4):
            if begin:
                expanded_key[:, 0] ^= key[:, 0]
                begin = False
            else:
                expanded_key[:, i] = expanded_key[:, i - 1] ^ key[:, i]

        # Ensure you stay within the bounds of the expanded_key array
        '''if current_round < rounds:
            expanded_key[:, current_round] = key'''
    print(expanded_key)

# Usage example
key = np.array([
        [0x2b, 0x28, 0xab, 0x09],
        [0x7e, 0xae, 0xf7, 0xcf],
        [0x15, 0xd2, 0x15, 0x4f],
        [0x16, 0xa6, 0x88, 0x3c]
    ], dtype=np.uint8)
key_expansion(key)