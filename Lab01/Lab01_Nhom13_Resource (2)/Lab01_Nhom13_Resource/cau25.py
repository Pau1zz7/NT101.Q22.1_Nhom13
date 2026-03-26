def encrypt(text, key):
    text = text.upper()
    key = key.upper()

    result = ""
    j = 0

    for i in range(len(text)):
        if text[i].isalpha():
            p = ord(text[i]) - 65
            k = ord(key[j % len(key)]) - 65
            result += chr((p + k) % 26 + 65)
            j += 1
        else:
            result += text[i]

    return result


def decrypt(cipher, key):
    cipher = cipher.upper()
    key = key.upper()

    result = ""
    j = 0

    for i in range(len(cipher)):
        if cipher[i].isalpha():
            c = ord(cipher[i]) - 65
            k = ord(key[j % len(key)]) - 65
            result += chr((c - k + 26) % 26 + 65)
            j += 1
        else:
            result += cipher[i]

    return result


# TEST
plaintext = "HELLO WORLD THIS IS A TEST MESSAGE"
key = "KEY"

cipher = encrypt(plaintext, key)

print("Plaintext:", plaintext)
print("Key:", key)
print("Encrypted:", cipher)

decrypted = decrypt(cipher, key)
print("Decrypted:", decrypted)