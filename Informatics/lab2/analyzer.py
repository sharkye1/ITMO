def decode_hamming_7_4(bits):
    if len(bits) != 7:
        return ("В коде должно быть ровно 7 бит", False)

    for b in bits:
        if b not in ("0", "1"):
            return ("Вообще-то код Хэмминга содержит только нули (0) и единички (1)", False)

    code = [int(b) for b in bits]

    r1 = code[0]
    r2 = code[1]
    i1 = code[2] 
    r3 = code[3]
    i2 = code[4] 
    i3 = code[5] 
    i4 = code[6] 

    s1 = r1 ^ i1 ^ i2 ^ i4
    s2 = r2 ^ i1 ^ i3 ^ i4
    s3 = r3 ^ i2 ^ i3 ^ i4

    err = int(str(s3) + str(s2) + str(s1), 2)
    if err != 0: return (f"Ошибка в бите {err}", True)
    return ("Ваш код не содержит ошибок", True)


    
if __name__ == "__main__":
    code = input("введите 7 бит подряд: ")
    res = decode_hamming_7_4(code)
    
    while not res[1]:
        print(res[0])
        code = input("введите 7 бит подряд: ")
        res = decode_hamming_7_4(code)
    
    print(res[0])
