## LAB 7: Web shell upload via obfuscated file extension

![2025-10-29-17-12-38](../images/2025-10-29-17-12-38.png)

>>-Phòng thí nghiệm này chứa một chức năng tải lên hình ảnh dễ bị tấn công. Một số phần mở rộng tệp bị đưa vào danh sách đen, nhưng biện pháp phòng thủ này có thể bị bỏ qua do một lỗi cơ bản trong cấu hình danh sách đen này.

>>-Để giải bài lab, hãy tải lên một web shell PHP cơ bản, sau đó sử dụng nó để trích xuất nội dung của tệp `/home/carlos/secret`. Gửi bí mật này bằng nút được cung cấp trong banner bài lab.

>>-Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: `wiener:peter`

![2025-10-29-17-15-46](../images/2025-10-29-17-15-46.png)

---

Gửi một file ảnh hợp lệ

---


![2025-10-29-17-24-00](../images/2025-10-29-17-24-00.png)

---

Khi gửi một file `webshell` với định dạng `php` thì  server từ chối

---

![2025-10-29-17-24-50](../images/2025-10-29-17-24-50.png)

---
 
Gửi file `.htaccess` cũng bị từ chối
 
---

![2025-10-29-17-25-32](../images/2025-10-29-17-25-32.png)
---
 
Sử dụng cả `.png` và `php` nếu server cho phép sử lí cả 2 định dạng

>>Upload thành công
 
---
![2025-10-29-17-27-35](../images/2025-10-29-17-27-35.png)
---
 
Nhưng khi vào thì chỉ thấy server sử lí hình ảnh còn không sử lí `php`
 
---

![2025-10-29-17-28-26](../images/2025-10-29-17-28-26.png)
---
 
`pwn.php.php` --> Xem server có kiểm tra kiểu `trim` đi `.php` không
 
---
![2025-10-29-17-28-48](../images/2025-10-29-17-28-48.png)
---
 
`pwn.p.phphp` --> Xem có `trim` đệ quy không
 
---
![2025-10-29-17-30-59](../images/2025-10-29-17-30-59.png)
---
 
Dùng `\0` nếu phần nhận thông tin thì vẫn coi `\0` là một kí tự còn phần sử lí đuôi file thì lại coi `\0` là kí tự kết thúc
>>200 OK
 
---
![2025-10-29-17-32-02](../images/2025-10-29-17-32-02.png)
---
 
Khi vào file `pwn.php` thì thấy mất đoạn payload `php`
>>Server đã thực thi đoạn code `php`
 
---
![2025-10-29-17-35-11](../images/2025-10-29-17-35-11.png)
---
 
Chỉnh sửa file `pwn.php` để đọc file `/etc/passwd`
 
---
![2025-10-29-17-35-43](../images/2025-10-29-17-35-43.png)
---
 
>>Đọc thành công file `/etc/passwd`
 
---

![2025-10-29-17-36-23](../images/2025-10-29-17-36-23.png)
---
 
Chỉnh để đọc file `/home/carlos/secret`
 
---
![2025-10-29-17-37-05](../images/2025-10-29-17-37-05.png)