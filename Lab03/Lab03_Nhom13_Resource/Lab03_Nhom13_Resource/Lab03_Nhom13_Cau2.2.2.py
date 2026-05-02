import hashlib

text_msg1 = """d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad3
40609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e315
6348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577
ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"""

text_msg2 = """d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad3
40609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e315
6348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577e
e8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"""

# 1. Xóa toàn bộ dấu xuống dòng (\n) và khoảng trắng bằng hàm replace()
hex_msg1 = text_msg1.replace('\n', '').replace(' ', '')
hex_msg2 = text_msg2.replace('\n', '').replace(' ', '')

# 2. Ép chuỗi văn bản Hex thành Dữ liệu Byte thô 
bytes_msg1 = bytes.fromhex(hex_msg1)
bytes_msg2 = bytes.fromhex(hex_msg2)

# 3. Tính băm MD5
hash1 = hashlib.md5(bytes_msg1).hexdigest()
hash2 = hashlib.md5(bytes_msg2).hexdigest()

print(f"MD5 của Message 1: {hash1}")
print(f"MD5 của Message 2: {hash2}")

if hash1 == hash2:
    print("\n=> Hai thông điệp đã tạo ra cùng một mã băm.")