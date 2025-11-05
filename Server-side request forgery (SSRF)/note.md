## LAB 1: Basic SSRF against the local server

__Tấn công SSRF cơ bản nhắm vào máy chủ cục bộ__

![2025-10-31-15-10-29](../images/2025-10-31-15-10-29.png)
---
 
>>Phòng thí nghiệm này có tính năng kiểm tra kho để lấy dữ liệu từ hệ thống nội bộ.\
>>Để giải quyết bài toán này, hãy thay đổi URL kiểm tra kho để truy cập vào giao diện quản trị tại `http://localhost/admin` và xóa người dùng `carlos`

---

![2025-10-31-15-13-49](../images/2025-10-31-15-13-49.png)
---
 
Khi check số lượng hàng còn lại thì có một `request` có tham số `stockApi` là một đường dẫn trong nội bộ web

 
---
![2025-10-31-15-15-26](../images/2025-10-31-15-15-26.png)
---
 
Thay đổi tham số `stockApi` thành `http://127.0.0.1` hoặc `http://localhost` để nó gọi đến chính nội bộ của nó\
Server trả về toàn bộ dao diện của `admin` 

 
---
![2025-10-31-15-31-43](../images/2025-10-31-15-31-43.png)
---
 
Chỉnh sửa URL thành `request` xóa user
 
---

![2025-10-31-15-31-57](../images/2025-10-31-15-31-57.png)

## LAB 2: Basic SSRF against another back-end system
____

![2025-10-31-15-40-01](../images/2025-10-31-15-40-01.png)
---
 
>>Phòng thí nghiệm này có tính năng kiểm tra kho, lấy dữ liệu từ hệ thống nội bộ.\
>>Để giải quyết bài tập, hãy sử dụng chức năng kiểm tra kho để quét `192.168.0.X` phạm vi nội bộ để tìm giao diện quản trị trên cổng `8080`, sau đó sử dụng nó để xóa người dùng `carlos`
 
---
![2025-10-31-15-44-37](../images/2025-10-31-15-44-37.png)
---
 
Khi check số lượng hàng thì có tham số cho phép lấy thông tin từ URL
 
---
![2025-10-31-15-46-51.png)](../images/2025-10-31-15-46-51.png)
---

Đề bài nói giao diện `admin` ở URL `http://192.168.0.X:8080` trong đó X chạy từ `1->254`\
Ý tưởng: BruceForce từ `1->154` 
 
---
![2025-10-31-15-52-48](../images/2025-10-31-15-52-48.png)
---
 
Khi chạy xong thấy có một request `X=18` trả về `200 OK` và có chứa cụm `Admin Panel`\
--> Địa chỉ của `admin panel` là `http://192.168.0.18:8080`

---
![2025-10-31-15-53-23](../images/2025-10-31-15-53-23.png)
---
 
Khi truy cập đến thì thấy có dao diện `admin`
 
---
![2025-10-31-15-54-11](../images/2025-10-31-15-54-11.png)
---
 
Sửa request để xóa user `carlos`
 
---
![2025-10-31-15-54-29](../images/2025-10-31-15-54-29.png)

## LAB 3: SSRF with blacklist-based input filter

__SSRF với filter kiểu blacklist__

![2025-10-31-16-08-06](../images/2025-10-31-16-08-06.png)
---
 
>>Phòng thí nghiệm này có tính năng kiểm tra kho để lấy dữ liệu từ hệ thống nội bộ.

>>Để giải quyết bài toán này, hãy thay đổi URL kiểm tra kho để truy cập vào giao diện quản trị tại `http://localhost/admin` và xóa người dùng `carlos`.

>>Nhà phát triển đã triển khai hai biện pháp phòng thủ chống SSRF yếu mà bạn sẽ cần phải vượt qua.

 
---

![2025-10-31-16-10-09](../images/2025-10-31-16-10-09.png)
---
 
Khi check hàng còn trong kho cho phép chèn URL để kiểm tra
 
---
![2025-10-31-16-10-56](../images/2025-10-31-16-10-56.png)
---
 
Chỉnh thành URL giao diện admin `http://localhost/admin`\
--> Nhưng bị chặn do server filter chuỗi nhạy cảm như `localhost` hay `admin`
 
---
![2025-10-31-16-11-26](../images/2025-10-31-16-11-26.png)
---
 
Thử đổi `localhost` thành `127.0.0.1`\
--> Vẫn bị filter
 
---
![2025-10-31-16-14-06](../images/2025-10-31-16-14-06.png)
---
 
Đổi IP thành số nguyên\
--> `400 Bad Request`\
Thay một chữ cái thường thành chữ cái hoa\
--> `Invalid host`
 
---
![2025-10-31-16-14-46](../images/2025-10-31-16-14-46.png)
---

Mã hóa URL chuỗi 
--> `400 Bad Request` 

---
![2025-10-31-16-15-47](../images/2025-10-31-16-15-47.png)
---
 

 
---
![2025-10-31-16-16-19](../images/2025-10-31-16-16-19.png)
---
 
Đổi IP thành số bát phân\
--> `400 Bad Request`
 
---
![2025-10-31-16-27-19](../images/2025-10-31-16-27-19.png)
---
 
Mã hóa URL 2 lần 
--> `200 OK`
 
---
![2025-10-31-16-27-55](../images/2025-10-31-16-27-55.png)
---
 
Sửa request để xóa user `carlos`
 
---
![2025-10-31-16-28-07](../images/2025-10-31-16-28-07.png)

## LAB 4: SSRF with filter bypass via open redirection vulnerability

__SSRF — vượt qua bộ lọc thông qua lỗ hổng chuyển hướng mở__

![2025-11-04-22-42-24](../images/2025-11-04-22-42-24.png)
---
 
>>Phòng thí nghiệm này có tính năng kiểm tra kho, lấy dữ liệu từ hệ thống nội bộ.

>>Để giải quyết bài toán này, hãy thay đổi URL kiểm tra kho để truy cập vào giao diện quản trị tại `http://192.168.0.12:8080/admin` và xóa người dùng `carlos`.

>>Trình kiểm tra kho đã bị hạn chế chỉ truy cập vào ứng dụng cục bộ, do đó, trước tiên bạn cần tìm một lệnh chuyển hướng mở ảnh hưởng đến ứng dụng.
 
---
![2025-11-04-22-52-58](../images/2025-11-04-22-52-58.png)
---
 
Truy cập vào và check stock nhưng tham số `stockAPI` không hề cho chuyển hướng 
 
---
![2025-11-04-22-43-25](../images/2025-11-04-22-43-25.png)
---
 
Thấy có `Next product` --> Truy cập và lấy request
 
---
![2025-11-04-22-44-06](../images/2025-11-04-22-44-06.png)
---
 
Ở đây có tham số `path` cho phép truyền vào một URL để chuyển hướng sang sản phẩm tiếp theo
 
---
![2025-11-04-22-45-00](../images/2025-11-04-22-45-00.png)
---
 
Truyền vào URL của đê bài --> `302`
 
---
![2025-11-04-22-45-35](../images/2025-11-04-22-45-35.png)
---
 
Sửa đổi để xóa `carlos`\
--> Thấy `302`
 
---
![2025-11-04-22-46-57](../images/2025-11-04-22-46-57.png)
---
 
Nhưng vẫn chưa thấy solve\
`nextProduct` chỉ redirect (302) — client thấy 302 nhưng backend có thể không follow → chưa xảy ra action.


`stockAPI` là server-side request (backend gọi URL bạn đưa) và thường follow redirect → có thể truy cập nội bộ và thực thi action.


Lấy giá trị `nextProduct` (open-redirect) dán vào `stockAPI` → server follow redirect → exploit thành công.


Tóm tắt 1 dòng: `302` thôi chưa đủ; cần server-side request + follow redirect để SSRF được.


 
---
![2025-11-04-22-50-03](../images/2025-11-04-22-50-03.png)
---
 
Truyền ULR của request `next product` vào tham số `stockAPI`\
--> Trả về giao diện `admin panel`
 
---
![2025-11-04-22-50-39](../images/2025-11-04-22-50-39.png)
---
 
Sửa request để xóa `carlos`
 
---
![2025-11-04-22-50-55](../images/2025-11-04-22-50-55.png)

## LAB 5: Blind SSRF with out-of-band detection

__SSRF mù — phát hiện bằng cơ chế out-of-band__

![2025-11-05-10-19-16](../images/2025-11-05-10-19-16.png)
---
 
>>Trang này dùng phần mềm phân tích (analytics) — khi một trang sản phẩm được tải, phần mềm sẽ fetch URL được ghi trong header Referer.\
>>Để giải lab, lợi dụng chức năng này để khiến một yêu cầu HTTP được gửi tới public Burp Collaborator server.
 
---
![2025-11-05-10-26-06](../images/2025-11-05-10-26-06.png)
---
 
Lấy một request khi xem sản phẩm\
Trong đó có `Referer`
 
---
![2025-11-05-10-26-40](../images/2025-11-05-10-26-40.png)
---
 
Thay bằng URL của `Burp Collaborator`
 
---
![2025-11-05-10-26-57](../images/2025-11-05-10-26-57.png)
---
 
Khi sang `Burp Collaborator` thấy có request gửi đến
 
---
![2025-11-05-10-27-22](../images/2025-11-05-10-27-22.png)