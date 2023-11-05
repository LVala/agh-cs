SBOX = [
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],
[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
],
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
],
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]
]

def ascii_to_binary(text: str) -> str:
    return "".join([bin(ord(i))[2:].zfill(8) for i in text])
    
def binary_to_ascii(binary: str) -> str:
    return "".join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])
    
def circular_left_shift(binary, num_of_bits):
     return binary[num_of_bits:] + binary[:num_of_bits]

def xor(first: str, second: str) -> str:
    return "".join(["0" if first[i] == second[i] else "1" for i in range(len(first))])

def generate_keys(key_binary: str) -> list[str]:
    # nie jesteśmy ograniczeni mocą sprzętową, więc
    # wygenerowane podklucze będą dłuższe
    # użyta zostanie również wariacja Triple DES,
    # gdzie do enkrypcji zostanie użyt pierwsza połowa klucza, a do dekrypcji druga
    # klucz wejściowy długości 128 bitów
    # klucze wyjściowe długości 48 bitów i będzie ich 10
    if len(key_binary) != 128: raise Exception("Length of the provided key is invalid")

    shifts = [1,3,2,1,1,1,2,1,2,1]
    permutations = [9,5,3,2,4,8,11,13,12,15,6,0]

    encrypt_key, decrypt_key = key_binary[:64], key_binary[64:]
    keys = {"encrypt_keys": [], "decrypt_keys": []}

    for name, key in zip(keys.keys(), [encrypt_key, decrypt_key]):
        # dzielimy na 16 bitowe kawałki
        keys_16 = [key[i:i+16] for i in range(0, len(key), 16)]
        for i in range(10):
            # przesunięcia bitowe PC1, każdy z keys_32 przesuwany o pewną różną dla każdego z keys_16 wartość z shifts
            new_key = ""
            for j in range(len(keys_16)):
                keys_16[j] = circular_left_shift(keys_16[j], shifts[(i+j)%10])
                # usuwamy po 4 elementy z każdego 16 bitowego kawałka
                new_key += "".join([keys_16[j][k] for k in permutations])
            
            keys[name].append(new_key)
            
    return keys

def expand(text: str) -> str:
    EXPANSION_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
        16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

    return "".join([text[i-1] for i in EXPANSION_TABLE])

def binary_to_decimal(binary):
    return int(binary,2)

def decimal_to_binary(decimal):
    return bin(decimal)[2:].zfill(4)

def substitute(text: str) -> str:
    text_6 = ["".join(text[i:i+6]) for i in range(0, len(text), 6)]
    result = ""

    for sbox_num, bit_6 in enumerate(text_6):
        first_last = binary_to_decimal(bit_6[0] + bit_6[-1])
        middle_4 = binary_to_decimal(bit_6[1:5])
        result += decimal_to_binary(SBOX[sbox_num][first_last][middle_4])

    return result

def permute(text: str) -> str:
    PERMUTATION_TABLE = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,
        2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

    return "".join([text[i-1] for i in PERMUTATION_TABLE])

def custom_F(text_binary: str, key_binary: str) -> str:
    # to samo co w DES, zrobiłbym ambitniejsze ale czasu brak
    expanded = expand(text_binary)
    mixed = xor(expanded, key_binary)
    substituted = substitute(mixed)
    permuted = permute(substituted)

    return permuted

def encrypt_once(binary_text: str, keys: list[str]) -> str:
    L, R = binary_text[:32], binary_text[32:]

    for key in keys:
        L, R = R, xor(L, custom_F(R, key))

    return L + R

def decrypt_once(binary_cipher: str, keys: list[str]) -> str:
    L, R = binary_cipher[:32], binary_cipher[32:]

    for key in reversed(keys):
        L, R = xor(R, custom_F(L, key)), L

    return L + R

def encrypt(ascii_text: str, key: str) -> str:
    keys = generate_keys(key)
    binary_text = ascii_to_binary(ascii_text)
    if len(binary_text) != 64: raise Exception("Length of the provided block is invalid")

    # enkrypcja z pierwszym zestawem kluczy
    # dekrypcja z drugim
    # ponowna enkrypcja z pierwszym zestawem
    cipher = encrypt_once(binary_text, keys["encrypt_keys"])
    cipher = decrypt_once(cipher, keys["decrypt_keys"])
    cipher = encrypt_once(cipher, keys["encrypt_keys"])

    return binary_to_ascii(cipher)

def decrypt(ascii_cipher: str, key: str) -> str:
    keys = generate_keys(key)
    binary_cipher = ascii_to_binary(ascii_cipher)
    if len(binary_cipher) != 64: raise Exception("Length of the provided block is invalid")

    text = decrypt_once(binary_cipher, keys["encrypt_keys"])
    text = encrypt_once(text, keys["decrypt_keys"])
    text = decrypt_once(text, keys["encrypt_keys"])

    return binary_to_ascii(text)

if __name__ == "__main__":
    plaintext = "krypto!?"
    key = "11001010101001010101110101101010100101011101100010101000101010010101001010101001001010100100101010100101010101101000101010100111"

    print("plaintext:", plaintext)
    cipher = encrypt(plaintext, key)
    print("cipher:", cipher)
    decrypted = decrypt(cipher, key)
    print("decrypted:", decrypted)
