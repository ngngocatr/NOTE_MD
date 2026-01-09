# CÀI ĐẶT WEB SITE VỚI GIAO THỨC HTTPS

Trước tiên tạo 2 folder:\
1. `/etc/ssl/nvngo2c_privates` --> Chứa key
2. `/etc/ssl/nvngo2c_certs` --> Chứa cert

Xin cấp _self cert_ bằng lệnh:\
`sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/nvngo2c_privates/nginx-selfsigned.key -out /etc/ssl/nvngo2c_certs/nginx-selfsigned.crt
`

--> Đầu ra _key_ là là file  `/etc/ssl/nvngo2c_privates/nginx-selfsigned.key`, đầu ra _cert_ là `/etc/ssl/nvngo2c_certs/nginx-selfsigned.crt`

--> Sau khi chạy lệnh xong thì nó hỏi các thông tin trước khi cấp _cert_
![2025-12-25-16-26-16](../../images/2025-12-25-16-26-16.png)

Sau đó cấu hình lại file config `nvngo2c_web.conf`
```
server{
    listen 443 ssl;
    server_name nvngo2c.com;

    ssl_certificate_key /etc/ssl/nvngo2c_privates/nginx-selfsigned.key;
    ssl_certificate /etc/ssl/nvngo2c_certs/nginx-selfsigned.crt;

    location /{
        root /usr/share/nginx/nvngo2c_web;
        index index.html;
    }
}

server{
    listen 80;
    server_name nvngo2c.com;
    return 301 https://$host$request_uri;
}
```
--> Cấu hình thành _HTTPS_ khi truy cập bằng _HTTP_ thì tự động chuyển hướng về _HTTPS_

Sau khi lưu file, kiểm tra bằng:\
`nginx -t`\
Nếu `ok` thì tiếp tục dùng reload để áp dụng những thay đổi:\
`sudo systemctl reload nginx`

Truy câp bằng `https://nvngo2c.com`
![2025-12-25-16-46-15](../../images/2025-12-25-16-46-15.png)

# CÀI ĐẶT WEB SITE VỚI WORDPRESS

## CÀI ĐẶT PHP
Cài đặt `PHP` để thực thi _Wordpress_\
`sudo dnf install -y php php-fpm php-mysqlnd php-gd php-xml php-mbstring php-curl php-zip`

Kích hoạt khởi động cùng hệ thống\
`sudo systemctl enable php-fpm`
![2025-12-25-16-54-36](../../images/2025-12-25-16-54-36.png)

Chỉnh sửa user cho `PHP-fpm`\
`sudo vi /etc/php-fpm.d/www.conf`

Sửa `user`, `group` thành `nginx`
![2025-12-25-16-59-03](../../images/2025-12-25-16-59-03.png)

Khởi động lại `PHP-fpm`\
`sudo systemctl restart php-fpm`

## CÀI ĐẶT MARIA_DB

Cài đặt Maria_DB\
`sudo dnf install -y mariadb-server`

Khởi động _MariaDB_\
`sudo systemctl start mariadb`

Khởi động cùng hệ thống\
`sudo systemctl enable mariadb`
![2025-12-25-17-02-54](../../images/2025-12-25-17-02-54.png)

Kiểm tra lại\
`sudo systemctl status mariadb`
![2025-12-25-17-10-24](../../images/2025-12-25-17-10-24.png)

Tạo DB cho _WordPress_\
`sudo mysql -u root -p`

Khởi tạo DB:
```SQL
CREATE DATABASE wpdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'matkhau123';
GRANT ALL PRIVILEGES ON wpdb.* TO 'wpuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
![2025-12-25-17-12-23](../../images/2025-12-25-17-12-23.png)

## CÀI ĐẶT WORDPRESS

Di chuyển đến thư mục `/tmp` và tải _WordPress_ về thư mục đó
```bash
cd /tmp
curl -O https://wordpress.org/latest.tar.gz
```
![2025-12-25-17-17-06](../../images/2025-12-25-17-17-06.png)

Giải nén\
`tar xzf latest.tar.gz`

![2025-12-25-17-18-37](../../images/2025-12-25-17-18-37.png)


Chuyển hết file từ `/tmp` sang `/usr/share/nginx/nvngo2c_web`\
```sh
sudo mv /tmp/wordpress/* .
``` 

![2025-12-25-17-22-27](../../images/2025-12-25-17-22-27.png)

Set người dùng và phân quyền
```sh 
sudo chown -R nginx:nginx /var/www/wordpress
sudo chmod -R 755 /var/www/wordpress
```

Sửa lại file config:
```nginx
server {
    listen 443 ssl;
    server_name nvngo2c.com;

    ssl_certificate     /etc/ssl/nvngo2c_certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/nvngo2c_privates/nginx-selfsigned.key;

    root /usr/share/nginx/nvngo2c_web;
    index index.php index.html index.htm;

    # WordPress pretty permalink
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # PHP handling
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/run/php-fpm/www.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    # deny access to hidden files
    location ~ /\. {
        deny all;
    }
}

server{
    listen 80;
    server_name nvngo2c.com;
    return 301 https://$host$request_uri;
}

```

Kiểm tra lại

![2025-12-25-17-41-51](../../images/2025-12-25-17-41-51.png)
--> OK

Nhưng khi truy cập vào lại báo là `Access denied.`
![2025-12-25-17-42-16](../../images/2025-12-25-17-42-16.png)

