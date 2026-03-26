import string
from collections import Counter

alphabet = string.ascii_uppercase

#LEAN TEXT
def clean_text(text):
    return ''.join([c for c in text.upper() if c.isalpha()])


#INDEX OF COINCIDENCE
def index_of_coincidence(text):
    N = len(text)
    freq = Counter(text)
    ic = sum(f*(f-1) for f in freq.values())
    return ic / (N*(N-1)) if N > 1 else 0


#GUESS KEY LENGTH
def guess_key_length(cipher, max_len=12):
    candidates = []

    print("=== IC Analysis ===")
    for k in range(1, max_len+1):
        groups = ['' for _ in range(k)]

        for i, c in enumerate(cipher):
            groups[i % k] += c

        avg_ic = sum(index_of_coincidence(g) for g in groups) / k
        print(f"Length {k}: {avg_ic:.4f}")

        if 0.06 <= avg_ic <= 0.075:
            candidates.append((k, avg_ic))

    best = min(candidates, key=lambda x: x[0])
    return best[0]

def score_english(text):
    common = "ETAOINSHRD"
    score = 0
    for c in text:
        if c in common:
            score += 1
    return score

def find_key(cipher, key_len):
    key = ""

    for i in range(key_len):
        group = cipher[i::key_len]

        best_shift = 0
        best_score = -1

        # thử tất cả 26 khả năng
        for shift in range(26):
            decrypted = ""

            for c in group:
                decrypted += chr((ord(c)-65-shift) % 26 + 65)

            score = score_english(decrypted)

            if score > best_score:
                best_score = score
                best_shift = shift

        key += chr(best_shift + 65)

    return key


# DECRYPT
def decrypt(cipher, key):
    result = ""
    j = 0

    for i in range(len(cipher)):
        c = ord(cipher[i]) - 65
        k = ord(key[j % len(key)]) - 65
        result += chr((c - k + 26) % 26 + 65)
        j += 1

    return result


#MAIN

cipher = """pp oiuibvql avpgzwm vyabnwzycbbg klhqla mv uqwckl kzzwktcfcwg hpp
wwftwzcktakah bxjjzcynlu pyzbcgp zzht omnpxtcfckts eahkxwve uvw
h uqn wy ywxy jtzgp wiejwxubbvpe wiesgp utzvtunpfz va nztuurizf
tgemizlu uh etfu fbim htq bikk va xmvprtyz mogey lxagdgqgpufck
tsialqmooe uzx buqx nhy edsxmviduxape wyg zlpqlimpqz uvw kkscbts
uuavbui mhl oltuzqvhvuiv mv rdibxjv pubt wtupivf yqv jkvyecvz vp
fbm buvqlvxa czx khuhuxmgakmf khtoghqvhvuivl zwob il jtqxqm jcdx
bkhpeukmpqzm igk gyuqe"""

cipher = clean_text(cipher)

key_len = guess_key_length(cipher)
print("\nChosen key length:", key_len)

key = find_key(cipher, key_len)
print("Key:", key)

plaintext = decrypt(cipher, key)

print("\nPlaintext:")
print(plaintext)