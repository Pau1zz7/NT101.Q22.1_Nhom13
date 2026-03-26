#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <array>
#include <algorithm>
#include <random>
#include <cmath>
#include <iomanip>

using namespace std;

double ENG_FREQ[26] = {
    8.2,1.5,2.8,4.3,12.7,2.2,2.0,6.1,7.0,0.15,
    0.77,4.0,2.4,6.7,7.5,1.9,0.1,6.0,6.3,9.1,
    2.8,0.98,2.4,0.15,2.0,0.07
};

const char* BIGRAMS[] = { "th","he","in","er","an","re","on","en","at","nd",
    "ti","es","or","te","of","ed","is","it","al","ar","st","to","nt","ng","se","ha","as","ou","ea","hi" };
int BG_SCORE[] = { 38,33,28,27,25,20,19,18,18,17,16,16,14,14,14,13,13,13,13,12,11,11,11,10,10,10,9,10,9,8 };

const char* TRIGRAMS[] = { "the","and","ing","ion","tio","ent","ati","for","her","ter","hat","tha","ere","con","all","ons" };
int TG_SCORE[] = { 168,76,73,56,53,55,50,42,41,38,38,36,34,34,29,29 };

using Key = array<int, 26>;

string caesarCipher(string text, int key) {
    key = (key % 26 + 26) % 26;
    string result = "";
    for (char c : text) {
        if (c >= 'A' && c <= 'Z') {
            result += char((c - 'A' + key) % 26 + 'A');
        }
        else if (c >= 'a' && c <= 'z') {
            result += char((c - 'a' + key) % 26 + 'a');
        }
        else {
            result += c;
        }
    }
    return result;
}

void bruteForceCaesar(string ciphertext) {
    for (int key = 1; key <= 25; key++) {
        string plaintext = caesarCipher(ciphertext, 26 - key);
        string lowerText = "";
        for (char c : plaintext) {
            lowerText += tolower(c);
        }

        if (lowerText.find(" the ") != string::npos) {
            cout << "Khoa K = " << key << "\n";
            cout << "Ban ro: \n" << plaintext << "\n";
            return;
        }
    }
    cout << "Khong tim thay ket qua phu hop!\n";
}

string apply_key(const string& text, const Key& key) {
    string r = text;
    for (char& c : r)
        if (c >= 'a' && c <= 'z') c = 'a' + key[c - 'a'];
    return r;
}

double score(const string& plain) {
    double s = 0;
    int n = plain.size();
    for (int i = 0; i + 1 < n; i++) {
        char a = plain[i], b = plain[i + 1];
        if (a < 'a' || a>'z' || b < 'a' || b>'z') continue;
        for (int k = 0; k < 30; k++)
            if (BIGRAMS[k][0] == a && BIGRAMS[k][1] == b) { s += log(BG_SCORE[k] + 1.0); break; }
    }
    for (int i = 0; i + 2 < n; i++) {
        char a = plain[i], b = plain[i + 1], c = plain[i + 2];
        if (a < 'a' || a>'z' || b < 'a' || b>'z' || c < 'a' || c>'z') continue;
        for (int k = 0; k < 16; k++)
            if (TRIGRAMS[k][0] == a && TRIGRAMS[k][1] == b && TRIGRAMS[k][2] == c) { s += log(TG_SCORE[k] + 1.0) * 2; break; }
    }
    return s;
}

Key init_key(const string& letters) {
    int freq[26] = {};
    for (char c : letters) freq[c - 'a']++;
    int ci[26], ei[26];
    for (int i = 0; i < 26; i++) ci[i] = ei[i] = i;
    sort(ci, ci + 26, [&](int a, int b) { return freq[a] > freq[b]; });
    sort(ei, ei + 26, [&](int a, int b) { return ENG_FREQ[a] > ENG_FREQ[b]; });
    Key key;
    for (int i = 0; i < 26; i++) key[ci[i]] = ei[i];
    return key;
}

Key solve(const string& norm) {
    string letters;
    for (char c : norm) if (c >= 'a' && c <= 'z') letters += c;

    mt19937 rng(42);
    uniform_int_distribution<int> pick(0, 25);

    Key best = init_key(letters);
    double best_sc = score(apply_key(letters, best));
    cout << "Score ban dau: " << fixed << setprecision(1) << best_sc << "\n\n";

    for (int r = 0; r < 15; r++) {
        Key cur = best;
        for (int n = 0; n < (r == 0 ? 0 : (r < 5 ? 3 : 6)); n++) {
            int a = pick(rng), b = pick(rng);
            while (b == a) b = pick(rng);
            swap(cur[a], cur[b]);
        }
        double cur_sc = score(apply_key(letters, cur));
        int no_improve = 0;

        for (int i = 0; i < 8000 && no_improve < 1500; i++) {
            int a = pick(rng), b = pick(rng);
            while (b == a) b = pick(rng);
            Key cand = cur; swap(cand[a], cand[b]);
            double ns = score(apply_key(letters, cand));
            if (ns > cur_sc) {
                cur = cand; cur_sc = ns; no_improve = 0;
                if (cur_sc > best_sc) { best_sc = cur_sc; best = cur; }
            }
            else no_improve++;
        }
        cout << "Restart " << setw(2) << r + 1 << "/15 | Score: " << fixed << setprecision(1) << best_sc << "\n";
    }
    return best;
}

int main() {
    while (true) {
        cout << "\n============================================\n";
        cout << "      HE THONG MA HOA & GIAI MA - PHAN 1    \n";
        cout << "============================================\n";
        cout << "1. Caesar Cipher (Ma hoa / Giai ma / Pha ma)\n";
        cout << "2. Mono-alphabetic Cipher (Giai ma tu dong)\n";
        cout << "0. Thoat chuong trinh\n";
        cout << "============================================\n";
        cout << "Chon chuc nang (0/1/2): ";

        int main_choice;
        if (!(cin >> main_choice)) {
            break;
        }
        cin.ignore();

        if (main_choice == 0) {
            cout << "Da thoat chuong trinh.\n";
            break;
        }
        else if (main_choice == 1) {
            int choice;
            cout << "\n[+] CAESAR CIPHER\n";
            cout << "1. Ma hoa\n2. Giai ma\n3. Brute-force\nChon chuc nang (1/2/3): ";
            cin >> choice;
            cin.ignore();

            if (choice == 1 || choice == 2) {
                string text;
                int key;
                cout << "Nhap chuoi van ban: ";
                getline(cin, text);
                cout << "Nhap khoa K: ";
                cin >> key;

                if (choice == 2) {
                    key = 26 - (key % 26);
                }
                cout << "Ket qua: " << caesarCipher(text, key) << "\n";
            }
            else if (choice == 3) {
                string ciphertext;
                cout << "Nhap ban ma can Brute-force: ";
                getline(cin, ciphertext);
                bruteForceCaesar(ciphertext);
            }
        }
        else if (main_choice == 2) {
            cout << "\n[+] MONO-ALPHABETIC CIPHER DECODER\n";
            int input_choice;
            string ciphertext = "";

            cout << "1. Nhap van ban tu ban phim\n2. Doc tu file\nChon chuc nang (1/2): ";
            cin >> input_choice;
            cin.ignore();

            if (input_choice == 2) {
                string filename;
                cout << "Nhap ten file (vd: data.txt): ";
                getline(cin, filename);
                ifstream f(filename);
                if (!f) {
                    cerr << "Khong mo duoc file!\n";
                    continue;
                }
                ostringstream ss; ss << f.rdbuf();
                ciphertext = ss.str();
                cout << "Doc tu file: " << filename << " (" << ciphertext.size() << " ky tu)\n\n";
            }
            else {
                cout << "Nhap ciphertext (Enter 2 lan lien tiep de bat dau):\n";
                string line;
                while (getline(cin, line)) {
                    if (line.empty()) break;
                    ciphertext += line + " ";
                }
            }

            if (ciphertext.empty()) {
                cout << "Loi: Khong co du lieu de xu ly.\n";
                continue;
            }

            string norm;
            for (char c : ciphertext)
                norm += isalpha(c) ? (char)tolower(c) : ' ';

            int freq[26] = {}, total = 0;
            for (char c : norm) if (c >= 'a' && c <= 'z') { freq[c - 'a']++; total++; }

            if (total == 0) {
                cout << "Loi: Khong tim thay chu cai hop le trong van ban.\n";
                continue;
            }

            int order[26]; for (int i = 0; i < 26; i++) order[i] = i;
            sort(order, order + 26, [&](int a, int b) { return freq[a] > freq[b]; });
            cout << "\nTop 10 ky tu pho bien nhat trong ciphertext:\n";
            for (int i = 0; i < 10; i++)
                cout << "  " << (char)('A' + order[i]) << ": " << fixed << setprecision(2)
                << 100.0 * freq[order[i]] / total << "%\n";
            cout << "Tong: " << total << " chu cai\n\n";

            Key key = solve(norm);

            cout << "\n--- ANH XA KHOA (Cipher -> Plain) ---\n";
            cout << "Cipher: "; for (int i = 0; i < 26; i++) cout << (char)('A' + i) << " "; cout << "\n";
            cout << "Plain:  "; for (int i = 0; i < 26; i++) cout << (char)('A' + key[i]) << " "; cout << "\n";

            cout << "\n--- BAN RO ---\n";
            string plain = apply_key(norm, key);
            int col = 0;
            for (char c : plain) { cout << c; if (++col % 80 == 0) cout << "\n"; }
            cout << "\n";

            ofstream out("output.txt"); out << plain;
            cout << "\nDa ghi vao output.txt\n";
        }
        else {
            cout << "Lua chon khong hop le!\n";
        }
    }
    return 0;
}