import math
import base64
import random
from sympy import isprime, nextprime

def modinv(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("e va phi khong nguyen to cung nhau")
    return x % phi

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def generate_rsa_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    assert math.gcd(e, phi) == 1, f"e={e} khong nguyen to cung nhau voi phi={phi}"
    d = modinv(e, phi)
    return (e, n), (d, n)

def rsa_encrypt_confidentiality(M, PU):
    e, n = PU
    return pow(M, e, n)

def rsa_decrypt_confidentiality(C, PR):
    d, n = PR
    return pow(C, d, n)

def rsa_encrypt_authentication(M, PR):
    d, n = PR
    return pow(M, d, n)

def rsa_decrypt_authentication(C, PU):
    e, n = PU
    return pow(C, e, n)

def int_to_bytes(n):
    length = max(1, (n.bit_length() + 7) // 8)
    return n.to_bytes(length, 'big')

def bytes_to_int(b):
    return int.from_bytes(b, 'big')

def encrypt_string_confidentiality(message: str, PU) -> str:
    e, n = PU
    key_bytes = (n.bit_length() + 7) // 8
    msg_bytes = message.encode('utf-8')
    M = bytes_to_int(msg_bytes)
    assert M < n, "Thong diep lon hon n, can chia khoi"
    C = pow(M, e, n)
    c_bytes = int_to_bytes(C)
    return base64.b64encode(c_bytes).decode()

def decrypt_string_confidentiality(b64_ciphertext: str, PR) -> str:
    d, n = PR
    c_bytes = base64.b64decode(b64_ciphertext)
    C = bytes_to_int(c_bytes)
    M = pow(C, d, n)
    return int_to_bytes(M).decode('utf-8')

def encrypt_string_authentication(message: str, PR) -> str:
    d, n = PR
    msg_bytes = message.encode('utf-8')
    M = bytes_to_int(msg_bytes)
    assert M < n, "Thong diep lon hon n"
    C = pow(M, d, n)
    return base64.b64encode(int_to_bytes(C)).decode()

def decrypt_string_authentication(b64_ciphertext: str, PU) -> str:
    e, n = PU
    c_bytes = base64.b64decode(b64_ciphertext)
    C = bytes_to_int(c_bytes)
    M = pow(C, e, n)
    return int_to_bytes(M).decode('utf-8')

def generate_random_rsa(bits=2048):
    half = bits // 2
    p = nextprime(random.getrandbits(half))
    q = nextprime(random.getrandbits(half))
    while q == p:
        q = nextprime(random.getrandbits(half))
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while math.gcd(e, phi) != 1:
        e = nextprime(e)
    d = modinv(e, phi)
    return (e, n), (d, n), p, q

def try_decrypt_all(ciphertext_b64_or_hex, all_keys, mode='base64'):
    results = []
    for label, PU, PR in all_keys:
        for scheme in ['confidentiality', 'authentication']:
            try:
                if mode == 'base64':
                    if scheme == 'confidentiality':
                        pt = decrypt_string_confidentiality(ciphertext_b64_or_hex, PR)
                    else:
                        pt = decrypt_string_authentication(ciphertext_b64_or_hex, PU)
                else: 
                    c_bytes = bytes.fromhex(ciphertext_b64_or_hex)
                    C = bytes_to_int(c_bytes)
                    if scheme == 'confidentiality':
                        d, n = PR
                        M = pow(C, d, n)
                    else:
                        e, n = PU
                        M = pow(C, e, n)
                    pt = int_to_bytes(M).decode('utf-8')
                
                if pt.isprintable():
                    results.append((label, scheme, pt))
            except Exception:
                pass
    return results

def decrypt_binary_string(bin_str: str, all_keys):
    bin_str = bin_str.strip().replace(' ', '').replace('\n', '')
    C = int(bin_str, 2)
    results = []
    for label, PU, PR in all_keys:
        for scheme in ['confidentiality', 'authentication']:
            try:
                if scheme == 'confidentiality':
                    d, n = PR
                    M = pow(C, d, n)
                else:
                    e, n = PU
                    M = pow(C, e, n)
                pt = int_to_bytes(M).decode('utf-8')
                if pt.isprintable():
                    results.append((label, scheme, pt))
            except Exception:
                pass
    return results

def section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def subsection(title):
    print(f"\n{'-'*60}")
    print(f"  {title}")
    print('-'*60)


section("PHAN 0: Sinh khoa RSA ngau nhien (khong cung cap p, q, e)")
PU_rand, PR_rand, p_rand, q_rand = generate_random_rsa(bits=2048)
print(f"p (512-bit, mot phan): {str(p_rand)[:40]}...")
print(f"q (512-bit, mot phan): {str(q_rand)[:40]}...")
print(f"PU = (e={PU_rand[0]}, n={str(PU_rand[1])[:40]}...)")
print(f"PR = (d={str(PR_rand[0])[:40]}..., n=...)")
print(f"Kich thuoc n: {PU_rand[1].bit_length()} bits")

section("PHAN 1: Xac dinh khoa cong khai PU va khoa rieng PR")

subsection("Bo khoa 1: p=11, q=17, e=7 (thap phan)")
p1, q1, e1 = 11, 17, 7
PU1, PR1 = generate_rsa_keys(p1, q1, e1)
n1 = p1 * q1
phi1 = (p1-1)*(q1-1)
print(f"n = p*q = {p1}*{q1} = {n1}")
print(f"phi(n) = (p-1)(q-1) = {p1-1}*{q1-1} = {phi1}")
print(f"gcd(e, phi(n)) = gcd({e1}, {phi1}) = {math.gcd(e1, phi1)}")
print(f"d = e^(-1) mod phi(n) = {PR1[0]}")
print(f"-> Khoa cong khai PU = (e={PU1[0]}, n={PU1[1]})")
print(f"-> Khoa rieng tu  PR = (d={PR1[0]}, n={PR1[1]})")

subsection("Bo khoa 2: p2, q2 lon, e2=17 (thap phan)")
p2 = 20079993872842322116151219
q2 = 676717145751736242170789
e2 = 17
PU2, PR2 = generate_rsa_keys(p2, q2, e2)
n2 = p2 * q2
phi2 = (p2-1)*(q2-1)
print(f"n = {n2}")
print(f"phi(n) = {phi2}")
print(f"d = {PR2[0]}")
print(f"-> PU = (e={PU2[0]}, n={PU2[1]})")
print(f"-> PR = (d={PR2[0]}, n={PR2[1]})")

subsection("Bo khoa 3: p3, q3, e3 (thap luc phan)")
p3 = int("F7E75FDC469067FFDC4E847C51F452DF", 16)
q3 = int("E85CED54AF57E53E092113E62F436F4F", 16)
e3 = int("0D88C3", 16)
PU3, PR3 = generate_rsa_keys(p3, q3, e3)
n3 = p3 * q3
phi3 = (p3-1)*(q3-1)
print(f"p3 = {hex(p3)}")
print(f"q3 = {hex(q3)}")
print(f"e3 = {hex(e3)} = {e3} (thap phan)")
print(f"n3 = {hex(n3)}")
print(f"d3 = {hex(PR3[0])}")
print(f"-> PU = (e={hex(PU3[0])}, n={hex(PU3[1])})")
print(f"-> PR = (d={hex(PR3[0])}, n={hex(PR3[1])})")

all_keys = [
    ("Bo khoa 1 (p1,q1,e1)", PU1, PR1),
    ("Bo khoa 2 (p2,q2,e2)", PU2, PR2),
    ("Bo khoa 3 (p3,q3,e3)", PU3, PR3),
]

section("PHAN 2: Ma hoa/Giai ma M=5 bang bo khoa 1 (p1=11, q1=17, e1=7)")
M = 5
subsection("2a. Ma hoa cho tinh bao mat (Confidentiality)")
C_conf = rsa_encrypt_confidentiality(M, PU1)
M_conf_dec = rsa_decrypt_confidentiality(C_conf, PR1)
print(f"Ban ro M = {M}")
print(f"Ma hoa:  C = M^e mod n = {M}^{PU1[0]} mod {PU1[1]} = {C_conf}")
print(f"Giai ma: M = C^d mod n = {C_conf}^{PR1[0]} mod {PR1[1]} = {M_conf_dec}")

subsection("2b. Ma hoa cho tinh xac thuc (Authentication)")
C_auth = rsa_encrypt_authentication(M, PR1)
M_auth_dec = rsa_decrypt_authentication(C_auth, PU1)
print(f"Ban ro M = {M}")
print(f"Ky (dung PR): C = M^d mod n = {M}^{PR1[0]} mod {PR1[1]} = {C_auth}")
print(f"Xac minh (dung PU): M = C^e mod n = {C_auth}^{PU1[0]} mod {PU1[1]} = {M_auth_dec}")

section("PHAN 3: Ma hoa chuoi 'The University of Information Technology' -> Base64")
message = "The University of Information Technology"
print(f"Thong diep: \"{message}\"")
print(f"Bytes: {message.encode('utf-8').hex()}")
M_str = bytes_to_int(message.encode('utf-8'))
print(f"M (so nguyen): {M_str}")

for label, PU, PR in all_keys:
    subsection(f"Dung {label}")
    e, n = PU
    if M_str < n:
        C_b64_conf = encrypt_string_confidentiality(message, PU)
        print(f"[Confidentiality - dung PU] Base64 ciphertext:\n  {C_b64_conf}")
        C_b64_auth = encrypt_string_authentication(message, PR)
        print(f"[Authentication  - dung PR] Base64 ciphertext:\n  {C_b64_auth}")
    else:
        print(f"  (Thong diep lon hon n={n}, bo qua bo khoa nay)")

section("PHAN 4: Tim ban ro cua cac ban ma cho san")

ciphertexts = {
    "CT-1 (Base64)": {
        "data": "raUcesUlOkx/8ZhgodMoo0Uu18sC20yXlQFevSu7W/FDxIy0YRHMyXcHdD9PBvIT2aUft5fCQEGomiVVPv4I",
        "mode": "base64"
    },
    "CT-2 (Hex)": {
        "data": "C87F570FC4F699CEC24020C6F54221ABAB2CE0C3",
        "mode": "hex"
    },
    "CT-3 (Base64)": {
        "data": "Z2BUSkJcg0w4XEpgm0JcMExEQmBlVH6dYEpNTHpMHptMQ7NgTHlgQrNMQ2BKTQ==",
        "mode": "base64"
    },
    "CT-4 (Binary)": {
        "data": "001010000001010011111111101101110010111011001010111011000110011110111111001111110110100011001111001100001001010001010100111101010100110011101110111011110101101100000100",
        "mode": "binary"
    },
}

for ct_name, ct_info in ciphertexts.items():
    subsection(f"Giai ma: {ct_name}")
    data = ct_info["data"]
    mode = ct_info["mode"]
    print(f"Ban ma: {data[:60]}{'...' if len(data)>60 else ''}")

    if mode == "binary":
        results = decrypt_binary_string(data, all_keys)
    else:
        results = try_decrypt_all(data, all_keys, mode=mode)

    if results:
        for lbl, scheme, pt in results:
            print(f"  -> [{lbl}] [{scheme}] Ban ro: \"{pt}\"")
    else:
        print("  -> Khong giai ma duoc voi bat ky bo khoa nao.")

print("\n" + "="*70)
print("  HOAN THANH NHIEM VU 2.1")
print("="*70)