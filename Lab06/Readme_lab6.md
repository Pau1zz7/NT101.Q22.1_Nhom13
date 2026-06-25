# Lab 06: Triển khai mạng Doanh nghiệp SME & Đánh giá rủi ro

##  Nội dung thực hiện chính

### 1. Thiết kế và Vận hành Hạ tầng
* **Sơ đồ Kiến trúc Mạng:** Xây dựng và triển khai sơ đồ mạng SME bảo mật.
* **Cấu hình pfSense Firewall:** * Thiết lập Bảng định tuyến và Tường lửa.
  * **Luật Ingress (WAN):** Áp dụng triết lý "Zero Trust" đối với luồng dữ liệu bên ngoài. Thực hiện thiết lập luật chặn toàn bộ (Block All) các kết nối chủ động từ Internet hướng vào WAN subnets.
  * **Mục đích:** Giúp hệ thống miễn nhiễm với rủi ro dò quét cổng (Port Scanning), ngăn chặn xâm nhập mạng trái phép hoặc khai thác lỗ hổng từ xa do công ty không cung cấp dịch vụ công khai nào trực tiếp qua IP WAN.

### 2. Đánh giá rủi ro & Đề xuất khắc phục bảo mật

Trong quá trình đánh giá hệ thống, nhóm đã phát hiện và xử lý các lỗ hổng sau:

####  Lỗ hổng 1: Dịch vụ Telnet truyền tải Cleartext
* **Mô tả:** Hệ thống sử dụng Telnet khiến mọi thông tin đăng nhập và dữ liệu truyền tải không được mã hóa. Kẻ tấn công có thể dùng kỹ thuật Man-in-the-Middle để nghe lén (eavesdrop) và đánh cắp thông tin. Ngoài ra, lỗi này còn làm lộ thông tin hệ điều hành (Ubuntu 20.04.6 LTS) qua lỗi Banner Grabbing.
* **Khắc phục:** Vô hiệu hóa hoàn toàn dịch vụ Telnet trên máy chủ nội bộ. Chuyển sang sử dụng giao thức SSH để mã hóa mọi phiên đăng nhập và luồng dữ liệu.

####  Lỗ hổng 2: mDNS Detection (Remote Network)
* **Mức độ rủi ro:** Medium
* **Mô tả:** Hệ thống mở cổng `5353/UDP` chạy giao thức mDNS. Dịch vụ này cho phép bên ngoài truy vấn và thu thập thông tin định danh máy chủ (như HĐH, danh sách dịch vụ, tên máy `pau-VirtualBox-2.local`). Kẻ tấn công có thể lạm dụng để thu thập thông tin (Reconnaissance) và lập bản đồ mạng.
* **Khắc phục:** Thiết lập cấu hình lọc (filter) trên tường lửa để chặn luồng dữ liệu đi vào cổng UDP 5353.