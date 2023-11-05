import pytest
from encrypt import aes_encryption, hex_string_to_array
from decrypt import aes_decryption

#reference: https://github.com/ircmaxell/quality-checker/blob/master/tmp/gh_18/PHP-PasswordLib-master/test/Data/Vectors/aes-ecb.test-vectors

key = hex_string_to_array('2b7e151628aed2a6abf7158809cf4f3c').transpose()

messages = [
    '6bc1bee22e409f96e93d7e117393172a',
    'ae2d8a571e03ac9c9eb76fac45af8e51',
    '30c81c46a35ce411e5fbc1191a0a52ef',
    'f69f2445df4f9b17ad2b417be66c3710'
]

ciphers = [
    '3ad77bb40d7a3660a89ecaf32466ef97',
    'f5d3d58503b9699de785895a96fdbaaf',
    '43b1cd7f598ece23881b00e3ed030688',
    '7b0c785e27e8ad3f8223207104725dd4'
]


@pytest.mark.parametrize("message, cipher", zip(messages, ciphers))
def test_encryption(message, cipher):
    message = hex_string_to_array(message).transpose()
    assert aes_encryption(10, message, key).hex() == cipher

@pytest.mark.parametrize("message, cipher", zip(messages, ciphers))
def test_decryption(message, cipher):
    cipher = hex_string_to_array(cipher).transpose()
    assert aes_decryption(10, cipher, key).hex() == message