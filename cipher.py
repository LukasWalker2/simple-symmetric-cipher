def cipher_gen(seed: int) -> int:
    length = len(format(seed, 'b'))
    possible_permutations = 2 ** length
    count = 0
    while count < possible_permutations:
        count += 1
        new_bit = (seed >> 1 ^ seed) & 1
        seed = seed >> 1 | new_bit << (length - 1)
        yield seed & 1

def crypt(key: str, to_crypt: bytes, min_ciphers: int, extra_ciphers: int) -> bytes:
    num_key = int.from_bytes(bytes(key, 'utf-8'))
    ciphers = [cipher_gen(num_key)]
    
    additional_ciphers = int(''.join([str(next(ciphers[-1])) for _ in range(256)]), 2) % (extra_ciphers + 1)
    
    for _ in range(min_ciphers + additional_ciphers):
        new_seed = int(''.join([str(next(ciphers[-1])) for _ in range(256)]), 2)
        ciphers.append(cipher_gen(new_seed))
    
    del ciphers[0]
    print(f'{len(ciphers)} ciphers used')
    message = b''
    for byte in to_crypt:
        num = ''
        for _ in range(8):
            xor_result = 0
            for cipher in ciphers:
                xor_result ^= next(cipher)
            num += str(xor_result)
        message += int.to_bytes(int(num,2) ^ byte)
    
    return message
