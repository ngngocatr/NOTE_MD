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

---
## LAB 5: Web shell upload via path traversal
__Tải web shell lên bằng cách lợi dụng lỗ hổng path traversal__

![2025-10-30-22-31-57](../images/2025-10-30-22-31-57.png)   
>>Phòng thí nghiệm này chứa một chức năng tải lên hình ảnh dễ bị tấn công. Máy chủ được cấu hình để ngăn chặn việc thực thi các tệp do người dùng cung cấp, nhưng hạn chế này có thể bị bỏ qua bằng cách khai thác lỗ hổng thứ cấp .

>>Để giải bài tập, hãy tải lên một web shell PHP cơ bản và sử dụng nó để trích xuất nội dung của tệp `/home/carlos/secret`. Gửi bí mật này bằng nút được cung cấp trong banner bài tập.

>>Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau:`wiener:peter`

![2025-10-30-22-16-10](../images/2025-10-30-22-16-10.png)
---
 
Gửi một file `php` lên thì `200 OK` ngay 
 
---
![2025-10-30-22-18-34](../images/2025-10-30-22-18-34.png)
---
 
Nhưng khi vào file thì thấy chỉ hiển thị nội dung của file
--> Trong thư mục chứa ảnh không có quyền chạy `php`
--> Phải upload file vào một thư mục có quyền chạy `php`

---
![2025-10-30-22-27-53](../images/2025-10-30-22-27-53.png)
---
 
Thử upload bằng `Path Traversal` nhưng server có vẻ như `trim` đi `../`

---
![2025-10-30-22-29-05](../images/2025-10-30-22-29-05.png)
---
 
Mã hóa `../` --> Đã upload được vào thư mục `/file`

---
![2025-10-30-22-29-26](../images/2025-10-30-22-29-26.png)
---
 
Thử truy cập vào file và thấy trả về nội dung của `/etc/passwd`
 
---
![2025-10-30-22-30-21](../images/2025-10-30-22-30-21.png)
---
 
Thay đổi nội dung của `pwn.php` và lấy nội dung từ `/home/carlos/secret`
 
---
![2025-10-30-22-30-48](../images/2025-10-30-22-30-48.png)

## LAB9 9:  Remote code execution via polyglot web shell upload

__Thực thi mã từ xa bằng cách tải lên web shell đa hình__

![2025-10-30-22-41-50](../images/2025-10-30-22-41-50.png)
---
 
>>Phòng thí nghiệm này chứa một hàm tải lên hình ảnh dễ bị tấn công. Mặc dù hàm này kiểm tra nội dung của tệp để xác minh đó là hình ảnh thật, nhưng vẫn có thể tải lên và thực thi mã phía máy chủ.

>>Để giải bài lab, hãy tải lên một web shell PHP cơ bản, sau đó sử dụng nó để trích xuất nội dung của tệp `/home/carlos/secret`. Gửi bí mật này bằng nút được cung cấp trong banner bài lab.

>>Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau:`wiener:peter`
 
---

![2025-10-30-22-44-21](../images/2025-10-30-22-44-21.png)
---
 
Gửi một file `webshell` lên"\
Nhưng bị từ chối
 
---
![2025-10-30-22-45-03](../images/2025-10-30-22-45-03.png)
---
 
Gửi với định dạng `.php.jpg` xem server có cho phép xử lí cả 2 loại không\
Nhưng vẫn bị từ chối
-->Vấn đề không ở tên file mà ở nội dung của file
 
---
![2025-10-30-22-45-57](../images/2025-10-30-22-45-57.png)
---
 
Gửi 1 file với nội dung của file ảnh nhưng tên lại có định dạng `php`
>>`200 OK`
 
---
![2025-10-30-22-46-37](../images/2025-10-30-22-46-37.png)
---
 
Chèn mã `php` vào trong nội dung của file ảnh

---
![2025-10-30-22-47-13](../images/2025-10-30-22-47-13.png)
---
 
Truy cập đến file ảnh và thấy được nội dung của file `/etc/passwd`
 
---
![2025-10-30-22-47-54](../images/2025-10-30-22-47-54.png)
---
 
Thay đổi payload và đọc nội dung của file `/home/carlos/secret`
 
---
![2025-10-30-22-48-23](../images/2025-10-30-22-48-23.png)