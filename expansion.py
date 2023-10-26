import numpy as np
from sbox import sub_bytes


def key_expansion(key, rounds):
    rcon = np.zeros(4, dtype=np.uint8)
    collection = [key]
    for i in range(0,rounds + 1):
        key,rcon = expand_round(key,i,rcon)
        collection.append(key)
        print(f"Chave{i}:\n {collection[i]}")
        #according to 14:37, 14:54, 15:07 its correct
    return collection

def expand_round(key,current_round,rcon):
    
    expanded_key = np.zeros((4, 4), dtype=np.uint8)
    rot_word = np.roll(key[:, 3], -1)
    np.set_printoptions(formatter={'int': hex})
    sub_word = sub_bytes(rot_word)
    if current_round == 0:
        rcon[0] = 0x01
    else:
        rcon[0] = 2 * rcon[0]
        if rcon[0] >= 0x80:
            rcon[0] ^= 0x11b

    # XOR the key with rcon
    expanded_key[:, 0] = rcon ^ sub_word

    begin = True
    for i in range(4):
        if begin:
            expanded_key[:, 0] ^= key[:, 0]
            begin = False
        else:
            expanded_key[:, i] = expanded_key[:, i - 1] ^ key[:, i]

    return expanded_key,rcon