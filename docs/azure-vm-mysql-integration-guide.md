# Azure Database for MySQL Flexible Server 설정 및 연동

## 1. Azure Database for MySQL Flexible Server 생성

```
1. Azure 포털 → 리소스 만들기 → "Azure Database for MySQL Flexible Server" 검색

2. 배포 옵션 선택
   - Flexible Server 선택 (권장)
   
3. 기본 설정
   - 구독: 사용 중인 구독 선택
   - 리소스 그룹: 기존 그룹 선택 또는 새로 생성
   - 서버 이름: food-classifier-db (예시)
   - 지역: Korea Central
   - MySQL 버전: 8.0
   
4. 인증 설정
   - 관리자 사용자 이름: myadmin (예시)
   - 암호: 복잡한 암호 설정 (기억하기!)
   
5. 네트워킹 설정
   - 연결 방법: 공용 액세스
   - 방화벽 규칙: Azure VM의 IP 주소 추가
```

## 2. Azure Database for MySQL Flexible Server의 네트워킹 설정

### 공용 액세스란?
- 데이터베이스 서버에 인터넷을 통해 접근 가능하도록 하는 설정
- 공개 IP 주소가 할당됨
- 기본적으로는 모든 접근이 차단되어 있음

### 방화벽 규칙 설정 방법

```
1. Azure 포털 접속
2. Azure Database for MySQL 서버 선택
3. 왼쪽 메뉴에서 "네트워킹" 선택
4. "방화벽 규칙" 섹션에서:
   - 규칙 이름: VM-Access
   - 시작 IP: [VM의 공용 IP 주소]
   - 종료 IP: [VM의 공용 IP 주소]
```

## 3. 데이터베이스 연결 테스트

```
# MySQL 클라이언트 설치 (VM에서)
sudo apt install mysql-client

# Azure MySQL 서버 연결
mysql -h food-classifier-db.mysql.database.azure.com -u myadmin -p
# 프롬프트가 나타나면 비밀번호 입력
```

## 4. 데이터베이스 생성 및 테이블 설정

### 데이터베이스 생성 및 선택

```
-- 데이터베이스 생성
CREATE DATABASE food_classifier;

-- 데이터베이스 목록 확인
SHOW DATABASES;

-- 생성한 데이터베이스 선택
USE food_classifier;
```

### 필요한 테이블 생성

```
-- 고객 테이블
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender ENUM('M', 'F'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 음식 영양 정보 테이블
CREATE TABLE food_nutrition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(100) UNIQUE NOT NULL,
    calories FLOAT,
    protein FLOAT,
    fat FLOAT,
    carbohydrate FLOAT,
    sodium FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 섭취 기록 테이블
CREATE TABLE consumption_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    food_id INT,
    consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (food_id) REFERENCES food_nutrition(id)
);

-- 테이블 생성 확인
SHOW TABLES;
```

### 테이블 구조 확인

```
-- 테이블 구조 확인
DESCRIBE customers;
DESCRIBE food_nutrition;
DESCRIBE consumption_logs;
```

### 초기 데이터 입력

```
-- 고객 데이터 샘플
INSERT INTO customers (customer_code, name, age, gender) VALUES
('CUST001', '김철수', 30, 'M'),
('CUST002', '이영희', 25, 'F');

-- 음식 영양 정보 샘플
INSERT INTO food_nutrition (food_name, calories, protein, fat, carbohydrate, sodium) VALUES
('김치찌개', 250, 15, 12, 20, 1200),
('비빔밥', 500, 20, 10, 85, 950);

-- 데이터 확인
SELECT * FROM customers;
SELECT * FROM food_nutrition;
```

## 5. 배포된 서비스와 연결하기 위해 필요한 환경 변수 설정

```
# 환경 변수 설정
AZURE_MYSQL_HOST=b006-food-decoder.mysql.database.azure.com
AZURE_MYSQL_DATABASE=food_classifier
AZURE_MYSQL_USER=team1lead
AZURE_MYSQL_PASSWORD=your_password_here
AZURE_MYSQL_SSL_CA=/etc/ssl/certs/DigiCertGlobalRootCA.crt.pem
```

### AZURE_MYSQL_SSL_CA

- Azure MySQL은 SSL 인증서가 필요한데, DigiCert Global Root CA 인증서를 다운로드하여 설정해야 합니다:

```
# SSL 인증서 다운로드
sudo curl -o /etc/ssl/certs/DigiCertGlobalRootCA.crt.pem https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem

# 인증서 권한 설정
sudo chmod 644 /etc/ssl/certs/DigiCertGlobalRootCA.crt.pem

# 인증서 위치 확인
ls -l /etc/ssl/certs/DigiCertGlobalRootCA.crt.pem
```

## 참고 문서
- [Azure Database for MySQL Flexible Server 공식 문서](https://learn.microsoft.com/ko-kr/azure/mysql/flexible-server/)
- [Azure Database for MySQL Flexible Server 네트워킹 가이드](https://learn.microsoft.com/ko-kr/azure/mysql/flexible-server/concepts-networking)
- [Azure Database for MySQL Flexible Server 보안 가이드](https://learn.microsoft.com/ko-kr/azure/mysql/flexible-server/how-to-connect-tls-ssl)