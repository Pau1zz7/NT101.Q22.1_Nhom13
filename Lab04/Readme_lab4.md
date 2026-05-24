# Lab 04: Quét lỗ hổng bảo mật với Nessus

## Mục tiêu
* Hiểu và biết cách sử dụng các công cụ quét lỗ hổng tự động thông dụng như Nessus, OpenVAS và Nmap[cite: 9].

## Nội dung chính
* **Quét cơ bản (Uncredentialed Scan):** Cấu hình template Basic Network Scan trên Nessus để quét tất cả các TCP port (1-65535) của mục tiêu Metasploitable 2 mà không dùng tài khoản đăng nhập[cite: 9].
* **Quét có xác thực (Credentialed Patch Audit):** Cung cấp thông tin đăng nhập SSH để Nessus đi sâu vào hệ điều hành, tìm các bản vá lỗi còn thiếu và ứng dụng lỗi thời[cite: 9].
* **Quét bằng Plugin chỉ định:** Tùy chỉnh Advanced Scan để chỉ kích hoạt một Plugin cụ thể (ví dụ: NFS Exported Share Information Disclosure) nhằm tiết kiệm thời gian và ẩn mình[cite: 9].
* **Phân tích Traffic:** Sử dụng Wireshark để giám sát các gói tin Nessus gửi đi trong quá trình thực hiện scan[cite: 9].

## Hướng dẫn sử dụng môi trường
1. **Khởi động mạng:** Bật máy ảo Kali Linux và máy mục tiêu Metasploitable 2 (đảm bảo chung dải mạng NAT 192.168.125.0/24)[cite: 9].
2. **Khởi động Nessus:** Trên máy Kali Linux, mở Terminal và khởi động dịch vụ bằng lệnh: `systemctl start nessusd`[cite: 9].
3. **Thao tác quét:** Truy cập giao diện web tại `https://localhost:8834/`, đăng nhập bằng tài khoản quản trị và thiết lập các bản quét tương ứng trong thư mục báo cáo[cite: 9].