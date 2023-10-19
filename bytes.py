#echo -n "abcdef" | openssl enc -e -a -aes-256-cbc -pass pass:YourPassword
import base64

def string_to_binary(string):    
    binary_string = ''
    binary_bytes = bytes(string, 'utf-8')
    for byte in binary_bytes:
        binary = bin(byte)[2:]  # indice ignora o 0b no inicio
        binary_string += binary.zfill(8) # faz um pad na esquerda se precisar para garantir 8 bits
    print(binary_string)
    return binary_string

def binary_to_string(binary):
    string = ''
    for byte in range(0,len(binary) - 1, 8):# indice ignora o 0b no inicio
        x = binary[byte:byte+8]
        string += chr(int(x, 2))
    print(string)
    return string

def xor(binary1, binary2):
    xored = ''
    if len(binary1) != len(binary2):
        raise ValueError("Xor between different size strings wont happen")
    for a,b in zip(binary1,binary2):
        xored += str(int(a) ^ int(b))
    print(xored)
    return xored

if __name__ == "__main__":
    a = string_to_binary('abcdef')
    b = string_to_binary('dsfsdf')
    xored = xor(a,b)
    binary_to_string(xored)

    '''
    binary_to_string('0101010001101000011001010010000001110001011101010110100101100011011010110010000001100010011100100110111101110111011011100010000001100110011011110111100000100000011010100111010101101101011100000111001100100000011011110111011001100101011100100010000000110001001100110010000001101100011000010111101001111001001000000110010001101111011001110111001100101110')
    print(base64.b64decode('VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIDEzIGxhenkgZG9ncy4='))
    '''