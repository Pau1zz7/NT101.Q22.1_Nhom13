def create_matrix(key):
    key = key.upper().replace(" ", "")
    key = key.replace("J", "I")

    result = []
    for c in key:
        if c not in result:
            result.append(c)

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for c in alphabet:
        if c not in result:
            result.append(c)

    matrix = [result[i:i+5] for i in range(0,25,5)]
    return matrix


def print_matrix(matrix):
    print("Playfair Matrix:")
    for row in matrix:
        print(" ".join(row))


def find_pos(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i,j


def decrypt(cipher, matrix):
    cipher = cipher.upper().replace(" ", "")
    cipher = cipher.replace("J", "I")

    result = ""

    for i in range(0, len(cipher), 2):
        a = cipher[i]
        b = cipher[i+1]

        r1,c1 = find_pos(matrix,a)
        r2,c2 = find_pos(matrix,b)

        if r1 == r2:
            result += matrix[r1][(c1-1)%5]
            result += matrix[r2][(c2-1)%5]

        elif c1 == c2:
            result += matrix[(r1-1)%5][c1]
            result += matrix[(r2-1)%5][c2]

        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result


key = "Harry Potter"

ciphertext = "ARYWYPHCBVEBYGMPNCYGCNTDNCWTMGRMFTQP LEWTMLREFBEBQEBIYGBFLPHVOAEHKDHEUNGQ FEROLEWTMLOPHEQGOSBEROQDWTLCMTHBWLNR KXRYLORYYPHCBVEBYRLGYDMKYGGWKLROANDB WGNERMNGYRLGHEWRTRLMBRHMUDGVODVTEGMC HLGWCMTFODNRRYCMZKODDUTDXGEOPOYRMFRM GUKXRYGHABROVTGQMCEHPRPEOTSEGEQLARYW YPOTMGQDOEXGOAUDHGUTULTNEHFTFHPGXGVP HGURBDMEGWKLETCBOTNTFQLTAEHMTUGEOAHE VEROXGVPHGDEWTEWGQIEDLPILERWPMOATNGQ KQEAHBMVRFKBRMKLXODXFREBHMNUKXRYKLRM FLWDDNCN"

matrix = create_matrix(key)
print_matrix(matrix)

print("\nDecrypted:")
print(decrypt(ciphertext, matrix))