# Lab 05: Khai thác tường lửa trong Linux (Linux Firewall Exploration)

## Mục tiêu
* Nắm vững cách thức hoạt động và triển khai tường lửa (Firewall) bảo vệ mạng nội bộ[cite: 8].
* Hiểu về thiết lập Virtual Private Network (VPN) và kỹ thuật sử dụng SSH Tunnel để vượt qua sự kiểm soát của tường lửa[cite: 8].

## Nội dung chính
* **Thiết lập Firewall Rules:** Cấu hình chính sách trên pfSense để chặn các gói tin Ping, HTTP (cổng 80), Telnet và ngăn truy cập các trang mạng xã hội từ máy nội bộ[cite: 8].
* **Vượt tường lửa (SSH Tunneling):** Thiết lập Local Port Forwarding để Telnet tới máy đích và Dynamic Port Forwarding (SOCKS5 proxy) để truy cập web bị chặn[cite: 8].
* **Application Firewall (Web Proxy):** Cài đặt và cấu hình Squid Proxy để kiểm soát truy cập web, đồng thời viết script Perl để chuyển hướng đường dẫn (URL Redirection) và thay thế hình ảnh trang web[cite: 8].
* **Triển khai VPN:** Cấu hình dịch vụ VPN trên pfSense để cho phép máy từ mạng ngoài (WAN) kết nối an toàn vào mạng nội bộ (LAN)[cite: 8].

## Hướng dẫn chạy môi trường mạng
1. **Khởi động hệ thống:** Yêu cầu bật đồng thời 3 máy ảo: Firewall (pfSense), Ubuntu VM A (mạng Host-only) và Ubuntu VM B (mạng NAT)[cite: 8].
2. **Thực thi Tunnel:** Trên Terminal của VM A, chạy lệnh SSH Tunnel (ví dụ: `ssh -fN -D 9000 ...`)[cite: 8].
3. **Cấu hình Trình duyệt:** Vào cài đặt Proxy của Firefox trên VM A, trỏ SOCKS5 Host về `127.0.0.1:9000` (hoặc cấu hình HTTP proxy về IP của máy Squid Server) để kiểm thử kết quả[cite: 8].