def decode_26(text, shift):
    res = []
    for c in text:
        if c.islower() and c in 'abcdefghijklmnopqrstuvwxyz':
            res.append(chr((ord(c) - 97 - shift) % 26 + 97))
        else:
            res.append(c)
    return "".join(res)

def decode_27(text, shift):
    res = []
    alf = 'abcdefghijklmnñopqrstuvwxyz'
    for c in text:
        if c in alf:
            res.append(alf[(alf.index(c) - shift) % 27])
        else:
            res.append(c)
    return "".join(res)

cipher = "larycxpajorj"
print("26 shift 9:", decode_26(cipher, 9))
print("27 shift 9:", decode_27(cipher, 9))
print("27 shift 10:", decode_27(cipher, 10))
print("27 shift 18:", decode_27(cipher, 18))
