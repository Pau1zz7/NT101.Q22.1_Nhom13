def encrypt(text, rails):
    text = text.replace(" ", "").upper()

    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction

        if rail == 0 or rail == rails - 1:
            direction *= -1

    result = ""
    for row in fence:
        result += ''.join(row)

    return result


def decrypt(cipher, rails):
    length = len(cipher)

    pattern = [['\n' for _ in range(length)] for _ in range(rails)]

    rail = 0
    direction = 1

    for i in range(length):
        pattern[rail][i] = '*'
        rail += direction

        if rail == 0 or rail == rails - 1:
            direction *= -1

    index = 0
    for i in range(rails):
        for j in range(length):
            if pattern[i][j] == '*' and index < length:
                pattern[i][j] = cipher[index]
                index += 1

    result = ""
    rail = 0
    direction = 1

    for i in range(length):
        result += pattern[rail][i]
        rail += direction

        if rail == 0 or rail == rails - 1:
            direction *= -1

    return result


plaintext = "HELLO WORLD THIS IS RAIL FENCE"
rails = 3

cipher = encrypt(plaintext, rails)

print("Plaintext:", plaintext)
print("Encrypted:", cipher)

decrypted = decrypt(cipher, rails)
print("Decrypted:", decrypted)