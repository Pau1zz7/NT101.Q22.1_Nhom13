# Lab 03: Hàm băm và Chữ ký số (Hash Functions and Digital Signatures)

## Mục tiêu
* Hiểu và phân tích các tính chất bảo mật của hàm băm một chiều và cơ chế xác thực thông điệp (MAC)[cite: 7].
* Đánh giá tác động của tấn công va chạm trên hàm băm yếu và thực hiện quy trình xác minh thủ công chứng chỉ số X.509[cite: 7].

## Nội dung chính
* **Mã hóa khóa công khai RSA:** Lập trình tạo khóa và mã hóa thông điệp nhiều khối cho cả hai trường hợp: tính bảo mật (Confidentiality) và tính xác thực (Authentication)[cite: 7].
* **Tấn công va chạm (Collision):** Quan sát và tạo giá trị băm MD5/SHA-1 cho các thông điệp và tập tin thực thi khác nhau nhưng có cùng giá trị băm[cite: 7].
* **Tạo va chạm MD5:** Sử dụng công cụ `md5collgen` để tạo ra hai tệp khác nhau từ cùng một tiền tố nhưng có chung mã băm MD5[cite: 7].
* **Xác minh chứng chỉ X.509:** Tải chứng chỉ từ máy chủ thực tế, trích xuất khóa công khai, chữ ký số, nội dung chứng chỉ bằng OpenSSL và viết script Python để xác minh thủ công[cite: 7].

## Hướng dẫn chạy chương trình
1. **Môi trường:** Sử dụng máy ảo Linux (hoặc Google Colab) đã cài sẵn Python 3.x và công cụ OpenSSL[cite: 7].
2. **Thực thi Script RSA:** Chạy các tệp mã nguồn Python để giải mã và mã hóa RSA.
3. **Thực thi lệnh OpenSSL:** Chạy các lệnh `openssl x509` và `openssl asn1parse` trên Terminal để trích xuất thông tin chứng chỉ `.pem` theo hướng dẫn trong thư mục[cite: 7].