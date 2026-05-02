import base64
import string
import random

# =========================
# 0. TOAN HOC RSA & SO NGUYEN TO (Bổ sung yêu cầu sinh khóa ngẫu nhiên)
# =========================
def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def modinv(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1: raise Exception("Khong co nghich dao")
    return x % phi

def calculate_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return (e, n), (d, n)

# Sinh số nguyên tố ngẫu nhiên (Miller-Rabin)
def is_prime(n, k=5):
    if n <= 1 or n == 4: return False
    if n <= 3: return True
    d = n - 1
    while d % 2 == 0: d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        while d != n - 1:
            x = pow(x, 2, n)
            d *= 2
            if x == 1: return False
            if x == n - 1: break
        else: return False
    return True

def generate_random_rsa(bits=512):
    def get_prime():
        while True:
            p = random.getrandbits(bits) | (1 << bits - 1) | 1
            if is_prime(p): return p
    p, q = get_prime(), get_prime()
    return calculate_keys(p, q, 65537)

# =========================
# TEXT FORMATTING
# =========================
def int_to_text(num):
    try: return num.to_bytes((num.bit_length()+7)//8, 'big').decode()
    except: return None

def is_valid_text(s):
    allowed = string.ascii_letters + string.digits + string.punctuation + " \n\r\t"
    return all(c in allowed for c in s) and len(s) > 3

# =========================
# SMART DECRYPT (FIX NULL BYTE & MULTI-BLOCK)
# =========================
# =========================
# SMART DECRYPT (NÂNG CẤP ĐẾM SỐ KHỐI & FIX NULL BYTE)
# =========================
def smart_decrypt(c_bytes, k, n):
    results = []

    # --- Single block (Nguyên khối) ---
    C = int.from_bytes(c_bytes, 'big')
    if C < n:
        M = pow(C, k, n)
        pt = int_to_text(M)
        if pt:
            pt = pt.replace('\x00', '')   # Xóa byte rỗng
            if is_valid_text(pt): results.append((pt, 1)) # Thêm số 1 (1 khối)

    # --- Multi-block (Đa khối) ---
    c_block_size = (n.bit_length() + 7) // 8
    if len(c_bytes) > c_block_size and len(c_bytes) % c_block_size == 0:
        p_bytes = b""
        valid = True
        num_blocks = len(c_bytes) // c_block_size
        
        if num_blocks > 1: # Phân biệt rõ với trường hợp 1 khối
            for i in range(0, len(c_bytes), c_block_size):
                chunk = int.from_bytes(c_bytes[i:i+c_block_size], 'big')
                if chunk >= n:
                    valid = False
                    break
                M_chunk = pow(chunk, k, n)
                p_bytes += M_chunk.to_bytes((M_chunk.bit_length()+7)//8, 'big')

            if valid:
                try:
                    pt = p_bytes.decode().replace('\x00', '')  # Xóa byte rỗng
                    if is_valid_text(pt): results.append((pt, num_blocks)) # Lấy số khối
                except: pass

    return results

# =========================
# ====== MAIN ============
# =========================

# -------------------------
# YÊU CẦU MỞ ĐẦU: SINH KHÓA NGẪU NHIÊN LỚN NHẤT CÓ THỂ
# -------------------------
print("\n========== 0. YEU CAU MO DAU: KHOA NGAU NHIEN ==========")
PU_rand, PR_rand = generate_random_rsa(bits=512)
print("-> Da sinh thanh cong cap khoa 1024-bits ngau nhien!")
print("PU_rand (e, n):", (PU_rand[0], str(PU_rand[1])[:40] + "..."))

msg_test = "Hello Security UIT"
msg_int = int.from_bytes(msg_test.encode(), 'big')
C_rand = pow(msg_int, PU_rand[0], PU_rand[1])
M_dec_rand = pow(C_rand, PR_rand[0], PR_rand[1])
print(f"-> Ma hoa ban ro '{msg_test}': Thanh cong!")
print(f"-> Giai ma khoi phuc lai: '{int_to_text(M_dec_rand)}'")

# -------------------------
# CAU 1: TAO 3 BO KHOA CO SAN
# -------------------------
print("\n========== 1. TAO KHOA (YEU CAU 1) ==========")
p1, q1, e1 = 11, 17, 7
PU1, PR1 = calculate_keys(p1, q1, e1)

p2, q2, e2 = 20079993872842322116151219, 676717145751736242170789, 17
PU2, PR2 = calculate_keys(p2, q2, e2)

p3 = int("F7E75FDC469067FFDC4E847C51F452DF", 16)
q3 = int("E85CED54AF57E53E092113E62F436F4F", 16)
e3 = int("0D88C3", 16)
PU3, PR3 = calculate_keys(p3, q3, e3)

print("PU1:", PU1, "PR1:", PR1)
print("PU2:", PU2, "PR2:", PR2)
print("PU3:", PU3, "PR3:", PR3)

# -------------------------
# CAU 2: M = 5
# -------------------------
print("\n========== 2. MA HOA M = 5 (YEU CAU 2) ==========")
M = 5
C = pow(M, PU1[0], PU1[1])
M_dec = pow(C, PR1[0], PR1[1])
S = pow(M, PR1[0], PR1[1])
M_auth = pow(S, PU1[0], PU1[1])

print("Confidentiality:", C, "->", M_dec)
print("Authentication:", S, "->", M_auth)

# -------------------------
# CAU 3: MA HOA CHUOI BASE 64 
# -------------------------
print("\n========== 3. MA HOA CHUOI (YEU CAU 3) ==========")
msg = "The University of Information Technology"
msg_bytes = msg.encode()

e, n = PU2   # PHẢI dùng key lớn
block_in = 31
block_out = (n.bit_length() + 7) // 8
cipher_bytes = b""

for i in range(0, len(msg_bytes), block_in):
    chunk = msg_bytes[i:i+block_in]
    m_int = int.from_bytes(chunk, 'big')
    c_int = pow(m_int, e, n)
    cipher_bytes += c_int.to_bytes(block_out, 'big')

cipher_b64 = base64.b64encode(cipher_bytes).decode()
print("Cipher Base64:", cipher_b64)

# -------------------------
# CAU 4: GIAI MA 
# -------------------------
print("\n========== 4. GIAI MA (YEU CAU 4) ==========")
ciphertexts = [
    ("CT1", "raUcesUlOkx/8ZhgodMoo0Uu18sC20yXlQFevSu7W/FDxIy0YRHMyXcHdD9PBvIT2aUft5fCQEGomiVVPv4I", "base64"),
    ("CT2", "C87F570FC4F699CEC24020C6F54221ABAB2CE0C3", "hex"),
    ("CT3", "Z2BUSkJcg0w4XEpgm0JcMExEQmBlVH6dYEpNTHpMHptMQ7NgTHlgQrNMQ2BKTQ==", "base64"),
    ("CT4", "001010000001010011111111101101110010111011001010111011000110011110111111001111110110100011001111001100001001010001010100111101010100110011101110111011110101101100000100", "binary")
]

all_keys = [("Key1", PU1, PR1), ("Key2", PU2, PR2), ("Key3", PU3, PR3)]

for name, data, mode in ciphertexts:
    print(f"\n--- Giai ma {name} ---")
    if mode == "base64": c_bytes = base64.b64decode(data)
    elif mode == "hex": c_bytes = bytes.fromhex(data)
    elif mode == "binary":
        c_int = int(data, 2)
        c_bytes = c_int.to_bytes((c_int.bit_length()+7)//8, 'big')

    found = False
    for label, PU, PR in all_keys:
        res1 = smart_decrypt(c_bytes, PR[0], PR[1]) # Thu Bao Mat
        for r in res1:
            print(f"[{label}] Bao mat:", r)
            found = True

        res2 = smart_decrypt(c_bytes, PU[0], PU[1]) # Thu Xac Thuc
        for r in res2:
            print(f"[{label}] Xac thuc:", r)
            found = True

    if not found: print("Khong giai duoc")