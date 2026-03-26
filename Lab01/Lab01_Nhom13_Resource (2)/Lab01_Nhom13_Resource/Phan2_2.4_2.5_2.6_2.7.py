import string
from collections import Counter

class PlayfairCipher:
    def __init__(self, key):
        self.matrix = self.create_matrix(key)

    def create_matrix(self, key):
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

    def print_matrix(self):
        print("Playfair Matrix:")
        for row in self.matrix:
            print(" ".join(row))

    def find_pos(self, char):
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == char:
                    return i,j

    def decrypt(self, cipher):
        cipher = cipher.upper().replace(" ", "")
        cipher = cipher.replace("J", "I")
        result = ""
        for i in range(0, len(cipher), 2):
            a = cipher[i]
            b = cipher[i+1]
            r1, c1 = self.find_pos(a)
            r2, c2 = self.find_pos(b)
            if r1 == r2:
                result += self.matrix[r1][(c1-1)%5]
                result += self.matrix[r2][(c2-1)%5]
            elif c1 == c2:
                result += self.matrix[(r1-1)%5][c1]
                result += self.matrix[(r2-1)%5][c2]
            else:
                result += self.matrix[r1][c2]
                result += self.matrix[r2][c1]
        return result

class VigenereCipher:
    def encrypt(self, text, key):
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

    def decrypt(self, cipher, key):
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

class VigenereCracker:
    def clean_text(self, text):
        return ''.join([c for c in text.upper() if c.isalpha()])

    def index_of_coincidence(self, text):
        N = len(text)
        freq = Counter(text)
        ic = sum(f*(f-1) for f in freq.values())
        return ic / (N*(N-1)) if N > 1 else 0

    def guess_key_length(self, cipher, max_len=12):
        candidates = []
        print("\n--- BANG PHAN TICH IC ---")
        for k in range(1, max_len+1):
            groups = ['' for _ in range(k)]
            for i, c in enumerate(cipher):
                groups[i % k] += c
            avg_ic = sum(self.index_of_coincidence(g) for g in groups) / k
            print(f"Do dai {k}: {avg_ic:.4f}")
            if 0.06 <= avg_ic <= 0.075:
                candidates.append((k, avg_ic))
        if not candidates:
            return 1
        best = min(candidates, key=lambda x: x[0])
        return best[0]

    def score_english(self, text):
        common = "ETAOINSHRD"
        score = 0
        for c in text:
            if c in common:
                score += 1
        return score

    def find_key(self, cipher, key_len):
        key = ""
        for i in range(key_len):
            group = cipher[i::key_len]
            best_shift = 0
            best_score = -1
            for shift in range(26):
                decrypted = ""
                for c in group:
                    decrypted += chr((ord(c)-65-shift) % 26 + 65)
                score = self.score_english(decrypted)
                if score > best_score:
                    best_score = score
                    best_shift = shift
            key += chr(best_shift + 65)
        return key

class RailFenceCipher:
    def encrypt(self, text, rails):
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

    def decrypt(self, cipher, rails):
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

def main():
    while True:
        print("\n" + "="*45)
        print("   HE THONG MA HOA & GIAI MA - PHAN 2")
        print("="*45)
        print("1. Playfair Cipher (Giai ma)")
        print("2. Vigenere Cipher (Ma hoa & Giai ma)")
        print("3. Vigenere Cracker (Pha ma tu dong)")
        print("4. Rail Fence Cipher (Ma hoa & Giai ma)")
        print("0. Thoat chuong trinh")
        print("="*45)
        
        choice = input("Chon chuc nang (0-4): ")
        
        if choice == '0':
            print("Da thoat chuong trinh.")
            break
            
        elif choice == '1':
            print("\n[+] PLAYFAIR CIPHER")
            key = input("Nhap khoa (Key): ")
            cipher_text = input("Nhap ban ma (Ciphertext): ")
            pf = PlayfairCipher(key)
            pf.print_matrix()
            print("Ban ro (Decrypted):", pf.decrypt(cipher_text))
            
        elif choice == '2':
            print("\n[+] VIGENERE CIPHER")
            action = input("Chon (1) Ma hoa hoac (2) Giai ma: ")
            text = input("Nhap van ban: ")
            key = input("Nhap khoa (Key): ")
            vg = VigenereCipher()
            if action == '1':
                print("Ban ma (Encrypted):", vg.encrypt(text, key))
            elif action == '2':
                print("Ban ro (Decrypted):", vg.decrypt(text, key))
                
        elif choice == '3':
            print("\n[+] VIGENERE CRACKER (Tu dong)")
            print("Nhap ban ma (Bam Enter 2 lan lien tiep de bat dau):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            cipher_text = "\n".join(lines)
            
            if not cipher_text.strip():
                continue
                
            vc = VigenereCracker()
            vg = VigenereCipher()
            clean_cipher = vc.clean_text(cipher_text)
            
            key_len = vc.guess_key_length(clean_cipher)
            print(f"\n=> Do dai khoa du doan tot nhat: {key_len}")
            
            key = vc.find_key(clean_cipher, key_len)
            print(f"=> Khoa (Key) tim duoc: {key}")
            
            print("\n--- BAN RO (DECRYPTED) ---")
            print(vg.decrypt(clean_cipher, key))
            
        elif choice == '4':
            print("\n[+] RAIL FENCE CIPHER")
            action = input("Chon (1) Ma hoa hoac (2) Giai ma: ")
            text = input("Nhap van ban: ")
            rails = int(input("Nhap so Rails (so nguyen): "))
            rf = RailFenceCipher()
            if action == '1':
                print("Ban ma (Encrypted):", rf.encrypt(text, rails))
            elif action == '2':
                print("Ban ro (Decrypted):", rf.decrypt(text, rails))
                
        else:
            print("Lua chon khong hop le, vui long nhap lai!")

if __name__ == "__main__":
    main()