## Lab 1: Exploiting an API endpoint using documentation
__Khai thác điểm cuối API bằng API documentation__

![2026-01-06-16-50-54](../../images/2026-01-06-16-50-54.png)
Lab yêu cầu tìm API bị lộ và xóa user `carlos`

Khi truy cập vào đường dẫn `https://0a35004c038754fd806a2b2300000064.web-security-academy.net/api/` thì ta thấy web có một bảng _REST API_ gồm 3 phương thức:

![2026-01-06-16-52-46](../../images/2026-01-06-16-52-46.png)

- GET: Lấy thông tin người dùng
![2026-01-06-16-54-46](../../images/2026-01-06-16-54-46.png)
![2026-01-06-16-55-08](../../images/2026-01-06-16-55-08.png)

- DELETE: Xóa người dùng
![2026-01-06-16-56-21](../../images/2026-01-06-16-56-21.png)

- PATCH: Thay đổi thông tin người dùng
![2026-01-06-16-58-33](../../images/2026-01-06-16-58-33.png)

Để giải quyết phòng này thì cần xóa user `carlos`\
Dùng method `DELETE`
![2026-01-06-16-59-42](../../images/2026-01-06-16-59-42.png)

Sau khi thực hiện server đã trả về `200` --> Xóa thành công user
![2026-01-06-16-59-53](../../images/2026-01-06-16-59-53.png)

![2026-01-06-17-00-44](../../images/2026-01-06-17-00-44.png)


## Lab 2: Finding and exploiting an unused API endpoint

__Tìm và khai thác điểm cuối API không sử dụng__

Lab yêu cầu mua được sản phẩm `Lightweight l33t Leather Jacket` với giá mong muốn
![2026-01-06-17-30-34](../../images/2026-01-06-17-30-34.png)

Khi truy cập chi tiết sản phẩm đó, ta thấy được có một request có path là : `/api/products/1/price` từ đây ta có thể biết được đường dẫn gọi API

![2026-01-06-17-31-22](../../images/2026-01-06-17-31-22.png)
![2026-01-06-17-31-54](../../images/2026-01-06-17-31-54.png)
![2026-01-06-17-36-29](../../images/2026-01-06-17-36-29.png)

Thử các method call API thì thấy chỉ có _GET_(ban đầu) trả về `200` và _PATCH_(thử) trả về `400` còn những method kia thì đều trả về `405 Method Not Allowed`
![2026-01-06-17-40-26](../../images/2026-01-06-17-40-26.png)
![2026-01-06-17-40-37](../../images/2026-01-06-17-40-37.png)

Method `PATCH` có thể thay đổi một phần dữ liệu\
Thông báo lỗi: _Only 'application/json' Content-Type is supported_\
--> Có hỗ trợ `Content-Type` và chỉ chấp nhận `application/json`--> Thiếu trường `Content-Type` và data khi dùng `PATCH`

Thấy được tham số gửi lên là `price`\
Ý tưởng là chỉnh sửa giá của sản phẩm bằng method `PATCH`
![2026-01-06-17-43-21](../../images/2026-01-06-17-43-21.png)

Thêm header `Content-Type` và chỉnh giá về `0`\
Gửi request thấy:
```JSON
{"price":"$0.00"}
```
![2026-01-06-17-45-18](../../images/2026-01-06-17-45-18.png)

Load lại trang thì thấy giá đã về `0`
![2026-01-06-17-46-56](../../images/2026-01-06-17-46-56.png)

Thêm sản phẩm vào giỏ hàng và mua
![2026-01-06-17-47-43](../../images/2026-01-06-17-47-43.png)

![2026-01-06-17-47-57](../../images/2026-01-06-17-47-57.png)

## Lab 3: Exploiting a mass assignment vulnerability

__Khai thác lỗ hổng gán giá trị hàng loạt__

Lab yêu cầu mua sán phẩm `Lightweight l33t Leather Jacket` với giá mong muốn
![2026-01-09-14-05-03](../../images/2026-01-09-14-05-03.png)

Ấn vào xem chi tiết sản phẩm cần mua
![2026-01-09-14-39-30](../../images/2026-01-09-14-39-30.png)

Thêm vào giỏ hàng\
Vẫn chưa có thông tin nhiều trong những request
![2026-01-09-14-40-18](../../images/2026-01-09-14-40-18.png)
![2026-01-09-14-41-48](../../images/2026-01-09-14-41-48.png)

Vào xem giỏ hàng, sang Burp Suite ta có thể thấy những request có path `/api/checkout` với method `GET` để lấy thông tin, tổng thanh toán của những mặt hàng đã thêm vào giỏ hàng
![2026-01-09-14-42-46](../../images/2026-01-09-14-42-46.png)
![2026-01-09-14-44-20](../../images/2026-01-09-14-44-20.png)

Xem chi tiết response trả về, thấy trả về dưới dụng _JSON_ và có 2 phần là `chosen_discount` và `chosen_products`
```JSON
{
    "chosen_discount":{"
        percentage":0},
    "chosen_products":[
        {
            "product_id":"1",
            "name":"Lightweight \"l33t\" Leather Jacket",
            "quantity":2,
            "item_price":133700
        }
    ]
}
```
![2026-01-09-14-50-41](../../images/2026-01-09-14-50-41.png)

Thử mua sản phẩm để tạo request mua\
Ta thấy web trả về lỗi không đủ tiền\
Nhưng có một request có path `/api/checkout` với method `POST` để thanh toán các sản phẩm trong giỏ hàng
```JSON
{
    "chosen_products":[
        {
            "product_id":"1",
            "quantity":2
        }
    ]
}
```
![2026-01-09-14-52-51](../../images/2026-01-09-14-52-51.png)

            "product_id":"1",
_Ý tưởng_: trong cả request `GET` và `POST` có thể thấy được có phần `chosen_products` nhưng trong request `POST` để thanh toán chỉ gồm có `product_id` và `quantity` mà trong đó có thể có cả `item_price`
--> Thêm tham số `item_price` với giá trị `0` --> Nếu đúng, web sẽ set giá của sản phẩm xuống `0`

Khi thực hiện, server đã trả về `201 Created` 
![2026-01-09-14-58-30](../../images/2026-01-09-14-58-30.png)

Nhưng khi kiểm tra lại giá của sản phẩm thì nó vẫn là giá gốc, không thay đổi
![2026-01-09-15-00-02](../../images/2026-01-09-15-00-02.png)

Dùng `Discover content` để quét xem còn những đường dẫn ẩn nào
![2026-01-09-15-02-03](../../images/2026-01-09-15-02-03.png)

Khi quét ta thấy được folder có tên là `doc` ở trong `api` --> Đây là `API Document`\
![2026-01-09-15-03-57](../../images/2026-01-09-15-03-57.png)

Nó gồm 3 đường dẫn
- `/api/doc/Order`: cho biết có 2 phần `ChosenProduct` và `ChosenDiscount`
![2026-01-09-15-05-23](../../images/2026-01-09-15-05-23.png)

- `/api/doc/ChosenProduct`: hướng dẫn về cách gọi api bằng các tham số cho phép về sản phẩm
![2026-01-09-15-06-00](../../images/2026-01-09-15-06-00.png)

- `/api/doc/ChosenDiscount`: hướng dẫn về cách gọi api bằng các tham số cho phép về mã giảm giá
![2026-01-09-15-06-30](../../images/2026-01-09-15-06-30.png)

_Ý tưởng_: Thêm phần `chosen_discount` vào trong request `POST` với tham số `percentage` (% giảm giá) là `100` để sản phẩm có thể được giảm giá `100%` khi thanh toán

Sau khi thực hiện, web vẫn trả về `201 Created`
![2026-01-09-15-15-12](../../images/2026-01-09-15-15-12.png)

Sau khi kiểm tra, bài đã được `Solve`, chứng tỏ rằng sản phẩm đã được thanh toán với phần trăm giảm giá `100%`
![2026-01-09-15-17-09](../../images/2026-01-09-15-17-09.png)

## Lab 4: Exploiting server-side parameter pollution in a query string
__Khai thác ô nhiễm tham số phía server trong chuỗi truy vấn__

Lab yêu cầu đăng nhập vào tài khoản `administrator` và xóa đi người dùng `carlos`
![2026-01-09-15-53-47](../../images/2026-01-09-15-53-47.png)

Sau khi thử tất cả các chức năng, không thấy có đường dẫn `\api` nào
![2026-01-09-16-50-04](../../images/2026-01-09-16-50-04.png)

Thử chức năng `Quên mật khẩu`\
Khi `Submit` thì thấy trả về đuôi của `email` mà account đó đăng kí
![2026-01-09-16-50-57](../../images/2026-01-09-16-50-57.png)
![2026-01-09-16-52-45](../../images/2026-01-09-16-52-45.png)

Response trả về khi gửi thông tin người dùng cần đổi mật khẩu
```JSON
{
    "type":"email",
    "result":"*****@normal-user.net"
}
```
![2026-01-09-16-53-42](../../images/2026-01-09-16-53-42.png)

Khi thêm một tham số đăng sau tham số `username` thì server trả về `Parameter is not supported` tức là không hỗ trợ tham số mà ta vừa thêm vào
>>csrf=afABwN8Gf2BcP6XJDlygRWILyRLElEDt&username=administrator&x=y
(thêm tham số `x`)

![2026-01-09-16-56-10](../../images/2026-01-09-16-56-10.png)

Thêm một dấu `#` vào để cắt đoạn tham số không được chấp nhận
>>username=administrator#&x=y

Server đã trả về một lỗi khác `Field not specified` tức là có một trường nào đó đã bị bỏ đi khi ta thêm dấu `#` vào\
--> Backend đã dựa vào dấu `#` để cắt đi những gì đằng sau của truy vấn --> Cắt luôn cả những thông tin đằng sau mà backend chủ động thêm vào sau chuỗi truy vấn
![2026-01-09-16-59-48](../../images/2026-01-09-16-59-48.png)

Thử thêm một tham số `filed` vào
>> username=administrator&field=x#&x=y

Server trả về
```JSON
{
    "type":"ClientError",
    "code":400,
    "error":"Invalid field."
}
```
Tức là tham số field tồn tại nhưng giá trị của nó lại không đúng
![2026-01-09-17-04-55](../../images/2026-01-09-17-04-55.png)

Vậy thì ta phải tìm kiếm xem những giá trị nào của tham số field thì web trả về dữ liệu

Chuyển request sang `Burp Intruder` để thực hiện _Brute Force_\
`Add` giá trị của tham số `field`
![2026-01-09-17-07-28](../../images/2026-01-09-17-07-28.png)

Ở phần `Payload configuration` chọn `Add from list` --> `Server-side variable names`
![2026-01-09-17-09-20](../../images/2026-01-09-17-09-20.png)
![2026-01-09-17-09-43](../../images/2026-01-09-17-09-43.png)
![2026-01-09-17-10-01](../../images/2026-01-09-17-10-01.png)

Ấn `Start attack` để bắt đầu _Brute Force_\
Kết quả chỉ thấy 2 biến là `username` và `email` trả về `200` và còn những biến khác thì đều không trả về dữ liệu `400`

Với payload `email`, server trả về đúng với dữ liệu ban đầu\
--> Điều này càng chứng tỏ rằng dấu `#` đã cắt bỏ đi những chuỗi còn lại đằng sau nó
![2026-01-09-17-15-04](../../images/2026-01-09-17-15-04.png)

Với payload `username`, server trả về dữ liệu là `username` của tài khoản đó
![2026-01-09-17-16-01](../../images/2026-01-09-17-16-01.png)

Check phần source ở URL `/static/js/forgotPassword.js` thấy có hàm
```JS
forgotPwdReady(() => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const resetToken = urlParams.get('reset-token');
    if (resetToken)
    {
        window.location.href = `/forgot-password?reset_token=${resetToken}`;
    }
    else
    {
        const forgotPasswordBtn = document.getElementById("forgot-password-btn");
        forgotPasswordBtn.addEventListener("click", displayMsg);
    }
});
```

Hàm này thực hiện việc chuyển hướng đến trang đổi mật khẩu `/forgot-password?reset_token=${resetToken}` khi có đúng `reset_token`

Thử thay giá trị của tham số `field` thành `reset_token`\
>>username=administrator&field=reset_token#&x=y

Server trả về giá trị của `reset_token`
![2026-01-09-17-21-24](../../images/2026-01-09-17-21-24.png)

Truy cập đường dẫn `/forgot-password?reset_token=(token vừa nhận được)`\
Ta được chuyển hướng đến một form để đổi mật khẩu
![2026-01-09-17-23-21](../../images/2026-01-09-17-23-21.png)

Đổi mật khẩu rồi đăng nhập vào tài khoản `administrator`\
Xóa user `carlos`
![2026-01-09-17-25-03](../../images/2026-01-09-17-25-03.png)
![2026-01-09-17-25-20](../../images/2026-01-09-17-25-20.png)
![2026-01-09-17-25-34](../../images/2026-01-09-17-25-34.png)


