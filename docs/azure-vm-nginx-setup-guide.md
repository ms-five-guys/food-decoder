# 🚀 Azure VM Nginx Setup Guide

> 이 가이드는 Azure VM에서 Nginx를 설정하고 SSL을 적용하는 과정을 설명합니다.

- 아래와 같은 문구를 보게 되었을 때 이 가이드를 참고하세요.

```
Welcome to nginx!
If you see this page, the nginx web server is successfully installed and working. Further configuration is required.

For online documentation and support please refer to nginx.org.
Commercial support is available at nginx.com.

Thank you for using nginx
```

## 1. 🛠️ Nginx 설치 및 기본 설정

### 1.1 Nginx 설치
```bash
sudo apt update
sudo apt install nginx
```

### 1.2 기본 설정 수정
```bash
# Nginx 설정 파일 열기
sudo vim /etc/nginx/sites-available/default

# 다음 설정으로 수정
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:7860;  # Gradio 앱 포트(다른 포트를 쓸 경우 변경)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 1.3 Nginx 재시작
```bash
# 설정 테스트
sudo nginx -t

# Nginx 재시작
sudo systemctl restart nginx
```

## 2. 🔒 SSL 설정 (HTTPS)

### 2.1 Certbot 설치
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

### 2.2 SSL 인증서 발급
```bash
sudo certbot --nginx -d your_domain.com
```

설정 과정:
1. 이메일 주소 입력
2. 약관 동의 (A)
3. 이메일 수신 여부 선택 (N)

### 2.3 최종 Nginx 설정 확인
```bash
sudo vim /etc/nginx/sites-available/default
```

예상되는 설정 내용:
```nginx
server {
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = your_domain.com) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name your_domain.com;
    return 404;
}
```

### 2.4 Nginx 재시작
```bash
sudo systemctl restart nginx
```

## 3. 🔄 유지보수

### 3.1 SSL 인증서 자동 갱신
- Let's Encrypt 인증서는 90일마다 갱신이 필요합니다.
- Certbot이 자동으로 갱신 작업을 처리합니다.
- 수동으로 갱신하려면:
```bash
sudo certbot renew
```

### 3.2 Nginx 상태 확인
```bash
sudo systemctl status nginx
```

### 3.3 로그 확인
```bash
# 에러 로그
sudo tail -f /var/log/nginx/error.log

# 액세스 로그
sudo tail -f /var/log/nginx/access.log
```

## 4. 🔧 문제 해결

### 4.1 Nginx 설정 테스트
```bash
sudo nginx -t
```

### 4.2 방화벽 설정 확인
```bash
# UFW 상태 확인
sudo ufw status

# 필요한 포트 열기
sudo ufw allow 80
sudo ufw allow 443
```

### 4.3 서비스 재시작
```bash
sudo systemctl restart nginx
```
