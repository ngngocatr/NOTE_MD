# REFLECTED XSS
## Lab 1: Reflected XSS into HTML context with nothing encoded

__XSS phản hồi, chèn thẳng vào HTML mà không hề được mã hoá__

![2025-11-19-19-36-12](../images/2025-11-19-19-36-12.png)

Lab yêu cầu thực thi hàm `alert` 

![2025-11-19-19-38-05](../images/2025-11-19-19-38-05.png)

Khi search một từ khóa nó sẽ được hiển thị lại 

![2025-11-19-19-39-13](../images/2025-11-19-19-39-13.png)

Khi xem trong DevTool thì thấy từ khóa đó được xuất hiện trong thẻ `h1`

![2025-11-19-19-42-36](../images/2025-11-19-19-42-36.png)

Khi chỉnh sửa payload thành `<script>alert('xss')</script>` thì thấy hàm được nằm ngay trong thẻ `h1`

![2025-11-19-19-43-31](../images/2025-11-19-19-43-31.png)

Hiện popup là kết quả của hàm `alert`

![2025-11-19-19-44-11](../images/2025-11-19-19-44-11.png)

## Lab 2: Stored XSS into HTML context with nothing encoded

__Stored XSS được nhét thẳng vào HTML mà không encode__

![2025-11-19-19-57-41](../images/2025-11-19-19-57-41.png)

Lab yêu cầu chèn code *Java Script* vào phần bình luận và làm nó thực thi mỗi khi có người vào xem bình luận

![2025-11-19-19-59-32](../images/2025-11-19-19-59-32.png)

Post một comment vào bài viết

![2025-11-19-20-01-01](../images/2025-11-19-20-01-01.png)

Khi vào xem comment đó thì thấy nó được hiển thị trong thẻ `h`

![2025-11-19-20-03-34](../images/2025-11-19-20-03-34.png)

Gửi một bình luận với nội dung: `<script>alert('xss')</script>`

![2025-11-19-20-04-09](../images/2025-11-19-20-04-09.png)

Khi vào lại trang bình luận thì thấy popup `XSS` là kết quả của hàm `alert`

![2025-11-19-20-04-41](../images/2025-11-19-20-04-41.png)

## Lab 3: Reflected XSS into HTML context with most tags and attributes blocked

__Reflected XSS trong ngữ cảnh HTML, nhưng hầu hết thẻ và thuộc tính đã bị chặn__

![2025-11-19-20-28-46](../images/2025-11-19-20-28-46.png)

Lab yêu cầu thực hiện hàm `print` trong khi web chặn hầu hết các thẻ và thuộc tính

![2025-11-19-20-32-12](../images/2025-11-19-20-32-12.png)

Khi dùng payload `<script>alert('xss')</script>` thì web chặn: **"Tag is not allowed"**

Chuyển payload sang `Intruder` và lấy list tag ở [XSS CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

![2025-11-19-20-42-44](../images/2025-11-19-20-42-44.png)

--> Start attack

![2025-11-19-20-43-09](../images/2025-11-19-20-43-09.png)

Hầu hết tất cả các tag đều bị chặn (`400`) nhưng có tag `body` và `custom tags` trả về `200`

