## Lab 1: Detecting NoSQL injection

__Phát hiện lỗ hổng NoSQL Injection__

![2025-12-26-14-59-24](../../images/2025-12-26-14-59-24.png)

Lab chứa lỗ hổng `NoSQLi` trong chức năng lọc sản phẩm, khai thác và in ra những sản phẩm chưa được phát hành

Khi gửi một request hợp lệ thì web vẫn trả về `200`
![2025-12-26-15-01-49](../../images/2025-12-26-15-01-49.png)

Nhưng khi thêm 1 dấu `'` thì web đã trả về `500`
![2025-12-26-15-03-03](../../images/2025-12-26-15-03-03.png)
![2025-12-26-15-05-08](../../images/2025-12-26-15-05-08.png)

--> Web đã xử lí không đúng dữ liệu do người dùng đưa vào
--> Nhìn vào lỗi trả về thì có thể thấy rằng web sử dụng `MongoDB`

Khi thêm payload có sử dụng điều kiện _Boolean_ chắc chắn đúng `'1'=='1'` thì web đã trả về `200`
![2025-12-26-15-07-42](../../images/2025-12-26-15-07-42.png)
![2025-12-26-15-08-15](../../images/2025-12-26-15-08-15.png)

Vậy là đã xác định được web có tồn tại `NoSQLi`
![2025-12-26-15-08-56](../../images/2025-12-26-15-08-56.png)

## Lab 2: Exploiting NoSQL operator injection to bypass authentication

__Khai thác lỗ hổng NoSQL Injection để vượt qua xác thực__

Lab yêu cầu khai thác lỗ hổng _NoSQL_ trong _MongoDB_ và login vào tài khoản của `admin`
![2025-12-26-15-30-57](../../images/2025-12-26-15-30-57.png)

Khi login vào tài khoản đã cho thì có thể thể thấy phần dữ liệu được gửi lên ở dạng _JSON_
![2025-12-26-15-34-52](../../images/2025-12-26-15-34-52.png)

Đổi trường _password_ thành `{"$ne":null}` và _username_ vẫn là `wiener` thì thấy web đã trả về `302` và trả về trang giao diện của người dùng `wiener`
![2025-12-26-15-44-42](../../images/2025-12-26-15-44-42.png)
![2025-12-26-15-45-15](../../images/2025-12-26-15-45-15.png)

Nhưng khi đăng nhập bằng tài khoản `administrator` thì web lại trả `Invalid username or password`
![2025-12-26-16-20-25](../../images/2025-12-26-16-20-25.png)

Thử bằng toán tử `regex`có tác dụng tìm chuỗi tương ứng với chuỗi đang có\
--> Dù chỉ biết `wien` nhưng vẫn có thể đăng nhập được vào
![2025-12-26-16-24-42](../../images/2025-12-26-16-24-42.png)

Đổi thành `admin.*`\
--> Thấy đã trả về `302` 
![2025-12-26-16-26-11](../../images/2025-12-26-16-26-11.png)

Nhưng vào bài thì vẫn chưa thấy _solve_
![2025-12-26-16-34-09](../../images/2025-12-26-16-34-09.png)


![2025-12-26-16-38-26](../../images/2025-12-26-16-38-26.png)
![2025-12-26-16-38-53](../../images/2025-12-26-16-38-53.png)
![2025-12-26-16-39-26](../../images/2025-12-26-16-39-26.png)

## Lab 3: Exploiting NoSQL injection to extract data

__Khai thác lỗ hổng NoSQL Injection để trích xuất dữ liệu__

Lab yêu cầu trích xuất mật khẩu của người dùng `administrator` và login vào tài khoản đó
![2025-12-26-16-46-39](../../images/2025-12-26-16-46-39.png)

Khi đăng nhập vào sẽ có sẵn một request check _role_ của người dùng
![2025-12-26-16-50-37](../../images/2025-12-26-16-50-37.png)

Khi đổi tên thành _administrator_ thì web trả về thông tin về quyền của người dùng `administrator`

Thử với 2 payload:
1. Người dùng không tồn tại `wiener1`\
--> Web trả về `Could not find user`
2. Người dùng với payload nhằm phá cấu trúc của request --> --> Web trả về `There was an error getting user details`
![2025-12-26-16-53-01](../../images/2025-12-26-16-53-01.png)
![2025-12-26-16-53-24](../../images/2025-12-26-16-53-24.png)
--> Web có tồn tại lỗi khi không xử lí đầu vào của người dùng

Ý tưởng để trích xuất được mật khẩu\

Làm một mệnh đề:\
__Người dùng chắc chắn có__ AND __Từng kí tự của mật khẩu__==__Từng chữ cái trong bảng chữ cái__ OR __Một mệnh đề chắc chắn sai__

Tức là:\ 
1. Người dùng chắc chắc có (_wiener_): `True`
2. Mệnh đề so sánh mật khẩu: 
    - Nếu đúng chữ cái đó: `True`
    - Nếu không: `False`
3. Mệnh đề chắc chắn sai : '1'=='0'

- Bởi nếu đúng chữ cái đó thì mệnh để có dạng\
`(True AND True) OR False` --> `True`\
--> Trả về quyền của người dùng\
- Nếu sai\
`(True AND False) OR False`\
--> Không trả về quyền của người dùng

Sử dụng payload:
`wiener' && this.password[0]=='' || '1'=='0` chuyển sang `Intruder` để _Brute Force_

Chuyển `Payload Type` sang `Brute Forcer`\
`Character set` chỉ cần những chữ cái thường\
`Min, max length`: 1 (_Vì chỉ cần kiểm tra từng kí tự_)
![2025-12-26-17-13-48](../../images/2025-12-26-17-13-48.png)

`Grep-Match` thêm một cột có chuỗi `"username": "wiener"` để xác định lúc nào mệnh đề đúng
![2025-12-26-17-16-06](../../images/2025-12-26-17-16-06.png)

__Start attack__\
Không thấy giá trị payload nào trả về _response_ có chứa chuỗi `"username": "wiener"`
--> Payload có vấn đề
![2025-12-26-17-17-11](../../images/2025-12-26-17-17-11.png)

_Encode URL_ payload\
![2025-12-26-17-18-49](../../images/2025-12-26-17-18-49.png)

__Start attack__\
Xuất hiện một hàng có giá trị tương ứng
![2025-12-26-17-19-15](../../images/2025-12-26-17-19-15.png)

Bây giờ cần kiểm tra độ dài của mật khẩu bằng payload\
`wiener' && this.password.length > 0 || '1'=='0`

Chuyển sang `Intruder` và set payload
![2025-12-26-17-26-03](../../images/2025-12-26-17-26-03.png)

__Start attack__\
Thấy rằng bắt đầu từ `5` thì xuất hiện `"Could not find user"`\
--> Mật khẩu có độ dài là `5`
![2025-12-26-17-28-09](../../images/2025-12-26-17-28-09.png)


Đã lấy được mật khẩu của người dùng `wiener` là peter
![2025-12-26-17-30-53](../../images/2025-12-26-17-30-53.png)
![2025-12-26-17-30-15](../../images/2025-12-26-17-30-15.png)

Thực hiện tương tự lấy được độ dài mật khẩu của `administrator` là `8`
![2025-12-26-17-32-56](../../images/2025-12-26-17-32-56.png)

Mật khẩu của `administrator`: `mcmrcwyk`
![2025-12-26-17-38-07](../../images/2025-12-26-17-38-07.png)

Đăng nhập vào để solve
![2025-12-26-17-39-19](../../images/2025-12-26-17-39-19.png)