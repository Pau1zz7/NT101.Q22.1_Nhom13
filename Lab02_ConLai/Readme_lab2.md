# Lab 02: Mật mã học hiện đại (Modern Cryptography)

## Mục tiêu
* Làm quen với các khái niệm trong mật mã học hiện đại, đặc biệt là hệ mật mã khối (DES, AES) và mật mã hóa khóa công khai (RSA)[cite: 10].
* Trải nghiệm trực quan về các chế độ hoạt động (Modes of operation), kỹ thuật đệm (padding), vector khởi tạo (IV) và hiệu ứng thác đổ (Avalanche effect)[cite: 10].

## Nội dung chính
* **Cấu trúc Feistel:** Triển khai một hệ mật mã Feistel đơn giản để quan sát sự lan truyền thay đổi của bit qua từng vòng[cite: 10].
* **Chế độ hoạt động (Mode of Operation):** Viết script mã hóa chuỗi lặp lại bằng AES-ECB và AES-CBC để phân biệt mức độ bảo mật[cite: 10].
* **Hiệu ứng thác đổ (Avalanche Effect):** Mã hóa bằng DES và đếm số lượng bit thay đổi (Hamming Distance) khi bản rõ hoặc khóa thay đổi[cite: 10].
* **Lan truyền lỗi:** Đảo bit trên bản mã AES-128 và giải mã để quan sát sự hỏng hóc dữ liệu trên các chế độ ECB, CBC, CFB, OFB[cite: 10].
* **Số nguyên tố lớn (RSA):** Lập trình tạo số nguyên tố lớn, tìm ước chung lớn nhất (GCD) bằng thuật toán Euclid và tính lũy thừa module cho mã hóa RSA[cite: 10].

## Hướng dẫn chạy chương trình
1. **Môi trường:** Đảm bảo máy tính có cài đặt Python 3.x[cite: 10].
2. **Cài đặt thư viện:** Chạy lệnh sau để cài đặt các thư viện cần thiết: 
   `pip install pycryptodome sympy numpy matplotlib`[cite: 10].
3. **Thực thi:** Mở Terminal/Command Prompt trong thư mục lab và chạy trực tiếp các script Python tương ứng cho từng bài tập (ví dụ: `python task2_1.py`).