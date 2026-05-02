import hashlib
import binascii

def bytes_to_int(b):
    return int.from_bytes(b, 'big')

def int_to_bytes(i, length=None):
    if length is None:
        length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, 'big')


BODY_FILE = "c0_body.bin"
SIG_FILE = "signature.hex"
E = 65537


N_HEX = "8F347587AF8472148D0710916F03ACF1D408359A19F29B1889346C988F7AD4DDEA05E8DE1B7C8C5412BA798AFB180D0D7C9CF3BD38E4A>

with open(BODY_FILE, "rb") as f:
    tbs = f.read()

computed_hash = hashlib.sha256(tbs).digest()

with open(SIG_FILE, "r") as f:
    sig_hex = f.read().strip()
signature = binascii.unhexlify(sig_hex)
n = int(N_HEX, 16)

em = pow(bytes_to_int(signature), E, n)
em_bytes = int_to_bytes(em, (n.bit_length() + 7) // 8)

extracted_hash = em_bytes[-32:]

print("Hash tính từ TBS          :", binascii.hexlify(computed_hash).decode())
print("Hash giải mã từ chữ ký    :", binascii.hexlify(extracted_hash).decode())

if computed_hash == extracted_hash:
    print("✅ CHỨNG CHỈ HỢP LỆ - Xác minh thành công!")
else:
    print("❌ Chữ ký KHÔNG hợp lệ!")
