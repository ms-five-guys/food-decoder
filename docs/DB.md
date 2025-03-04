# 고객 데이터 삽입

```sql
USE food_tracking;
```

## 1. 고객 정보 테이블

### 테이블 생성

```sql
CREATE TABLE customer(
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    age INT NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    photo_url VARCHAR(255),
    notes TEXT
);
```

### 데이터 삽입

```sql
INSERT INTO customer (name, gender, age, height, weight, photo_url, notes)
VALUES
('김기덕', '940127-123123', 'M', 75, 183, 74, '/mnt/batch/tasks/shared/LS_root/mounts/clusters/heejuaml-instance/code/Users/6b040/data/김기덕.jpg', '고혈압이 있음. 짠 음식 주의 필요.'),
('김민석', '000604-123123', 'M', 79, 178, 73, '/mnt/batch/tasks/shared/LS_root/mounts/clusters/heejuaml-instance/code/Users/6b040/data/김민석.jpg', '당뇨 있음. 단 음식 조절 필요.'),
('박현열', '971010-123123', 'M', 84, 174, 79, '/mnt/batch/tasks/shared/LS_root/mounts/clusters/heejuaml-instance/code/Users/6b040/data/박현열.jpg', '신장이 안 좋음. 염분과 단백질 섭취 제한 필요.'),
('윤소영', '020511-123123', 'F', 71, 165, 52, '/mnt/batch/tasks/shared/LS_root/mounts/clusters/heejuaml-instance/code/Users/6b040/data/윤소영.jpg', '관절염 있음. 무리한 운동 금지.'),
('이희주', '020330-123123', 'F', 87, 168, 57, '/mnt/batch/tasks/shared/LS_root/mounts/clusters/heejuaml-instance/code/Users/6b040/data/이희주.jpg', '소화가 약함. 기름진 음식 자제, 소화 잘되는 음식 제공.');
```

### 테이블 확인

```sql
-- 테이블 구조 확인
DESCRIBE customer;

-- 테이블 데이터 확인
SELECT * FROM customer;
```

## 2. notes 정보별 권장 섭취량 기준 테이블

> 고혈압 → hypertension_diet: 저염식

> 당뇨 → diabetes_diet: 저탄수화물, 저당

> 신장질환 → kidney_diet: 저염, 저단백

> 관절염 → arthritis_diet: 일반식 (특별한 제한 없음)

> 소화약함 → digestive_diet: 저지방

### 테이블 생성

```sql
CREATE TABLE recommended_nutrition (
    nutrition_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    diet_type ENUM('hypertension_diet', 'diabetes_diet', 'kidney_diet', 'arthritis_diet', 'digestive_diet') NOT NULL,
    Energy_min FLOAT NOT NULL,
    Energy_max FLOAT NOT NULL,
    Carbohydrates_min FLOAT NOT NULL,
    Carbohydrates_max FLOAT NOT NULL,
    Protein_min FLOAT NOT NULL,
    Protein_max FLOAT NOT NULL,
    Fat_min FLOAT NOT NULL,
    Fat_max FLOAT NOT NULL,
    Dietary_Fiber_min FLOAT NOT NULL,
    Dietary_Fiber_max FLOAT NOT NULL,
    Sodium_min FLOAT NOT NULL,
    Sodium_max FLOAT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
```

### 데이터 삽입

```sql
-- 각 diet type별 권장 섭취량 입력 (예시 값)
INSERT INTO recommended_nutrition 
(customer_id, diet_type, 
 Energy_min, Energy_max, 
 Carbohydrates_min, Carbohydrates_max,
 Protein_min, Protein_max,
 Fat_min, Fat_max,
 Dietary_Fiber_min, Dietary_Fiber_max,
 Sodium_min, Sodium_max) 
VALUES
-- 고혈압 (저염식)
(1, 'hypertension_diet', 
 1800, 2200,    -- Energy
 250, 300,      -- Carbohydrates
 60, 80,        -- Protein
 40, 60,        -- Fat
 25, 30,        -- Dietary_Fiber
 1500, 2000),   -- Sodium (제한)

-- 당뇨 (저탄수화물)
(2, 'diabetes_diet',
 1800, 2200,    -- Energy
 200, 250,      -- Carbohydrates (제한)
 70, 90,        -- Protein
 50, 70,        -- Fat
 25, 30,        -- Dietary_Fiber
 2000, 2300),   -- Sodium

-- 신장질환 (저염, 저단백)
(3, 'kidney_diet',
 1800, 2200,    -- Energy
 250, 300,      -- Carbohydrates
 40, 50,        -- Protein (제한)
 50, 70,        -- Fat
 20, 25,        -- Dietary_Fiber
 1500, 2000),   -- Sodium (제한)

-- 관절염 (일반식)
(4, 'arthritis_diet',
 1800, 2200,    -- Energy
 250, 300,      -- Carbohydrates
 60, 80,        -- Protein
 50, 70,        -- Fat
 25, 30,        -- Dietary_Fiber
 2000, 2300),   -- Sodium

-- 소화약함 (저지방)
(5, 'digestive_diet',
 1800, 2200,    -- Energy
 250, 300,      -- Carbohydrates
 60, 80,        -- Protein
 30, 50,        -- Fat (제한)
 20, 25,        -- Dietary_Fiber
 2000, 2300);   -- Sodium
```

### 테이블 확인

```sql
-- 테이블 구조 확인
DESCRIBE recommended_nutrition;

-- 테이블 데이터 확인
SELECT * FROM recommended_nutrition;
```

## 3. 음식 정보 테이블

### 테이블 생성

```sql
CREATE TABLE nutrition_info(
food_id INT AUTO_INCREMENT PRIMARY KEY,
food_name VARCHAR(100),
Energy FLOAT NOT NULL,
Carbohydrates FLOAT NOT NULL,
Protein FLOAT NOT NULL,
Fat FLOAT NOT NULL,
Dietary_Fiber FLOAT NOT NULL,
Sodium FLOAT NOT NULL);
```

### 데이터 삽입

```sql
INSERT INTO nutrition_info (food_name, Energy, Carbohydrates, Protein, Fat, Dietary_Fiber, Sodium)
VALUES
('김치찌개', 45, 1.04, 4.25, 2.71, 1.5, 207),
('비빔밥', 142, 18.84, 6.86, 4.32, 2.0, 232);
```

### 테이블 확인

```sql
-- 테이블 구조 확인
DESCRIBE nutrition_info;

-- 테이블 데이터 확인
SELECT * FROM nutrition_info;
```

## 4. 섭취 이력 테이블

### 테이블 생성

```sql
CREATE TABLE consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    food_id INT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES nutrition_info(food_id) ON DELETE CASCADE
);
```

### 데이터 삽입

```sql
INSERT INTO consumption (customer_id, food_id, time, date)
VALUES
(1, 1, '2025-02-17 08:00:00', '2025-02-17'),
(1, 2, '2025-02-17 13:00:00', '2025-02-17'),
(1, 1, '2025-02-17 18:00:00', '2025-02-17'),

(2, 1, '2025-02-17 08:00:00', '2025-02-17'),
(2, 2, '2025-02-17 13:00:00', '2025-02-17'),
(2, 1, '2025-02-17 18:00:00', '2025-02-17'),

(3, 1, '2025-02-17 08:00:00', '2025-02-17'),
(3, 2, '2025-02-17 13:00:00', '2025-02-17'),
(3, 1, '2025-02-17 18:00:00', '2025-02-17'),

(4, 1, '2025-02-17 08:00:00', '2025-02-17'),
(4, 2, '2025-02-17 13:00:00', '2025-02-17'),
(4, 1, '2025-02-17 18:00:00', '2025-02-17'),

(5, 1, '2025-02-17 08:00:00', '2025-02-17'),
(5, 2, '2025-02-17 13:00:00', '2025-02-17'),
(5, 1, '2025-02-17 18:00:00', '2025-02-17'),

(1, 1, '2025-02-18 08:00:00', '2025-02-18'),
(1, 2, '2025-02-18 13:00:00', '2025-02-18'),
(1, 1, '2025-02-18 18:00:00', '2025-02-18'),

(2, 1, '2025-02-18 08:00:00', '2025-02-18'),
(2, 2, '2025-02-18 13:00:00', '2025-02-18'),
(2, 1, '2025-02-18 18:00:00', '2025-02-18'),

(3, 1, '2025-02-18 08:00:00', '2025-02-18'),
(3, 2, '2025-02-18 13:00:00', '2025-02-18'),
(3, 1, '2025-02-18 18:00:00', '2025-02-18'),

(4, 1, '2025-02-18 08:00:00', '2025-02-18'),
(4, 2, '2025-02-18 13:00:00', '2025-02-18'),
(4, 1, '2025-02-18 18:00:00', '2025-02-18'),

(5, 1, '2025-02-18 08:00:00', '2025-02-18'),
(5, 2, '2025-02-18 13:00:00', '2025-02-18'),
(5, 1, '2025-02-18 18:00:00', '2025-02-18'),

(1, 1, '2025-02-19 08:00:00', '2025-02-19'),
(1, 2, '2025-02-19 13:00:00', '2025-02-19'),
(1, 1, '2025-02-19 18:00:00', '2025-02-19'),

(2, 1, '2025-02-19 08:00:00', '2025-02-19'),
(2, 2, '2025-02-19 13:00:00', '2025-02-19'),
(2, 1, '2025-02-19 18:00:00', '2025-02-19'),

(3, 1, '2025-02-19 08:00:00', '2025-02-19'),
(3, 2, '2025-02-19 13:00:00', '2025-02-19'),
(3, 1, '2025-02-19 18:00:00', '2025-02-19'),

(4, 1, '2025-02-19 08:00:00', '2025-02-19'),
(4, 2, '2025-02-19 13:00:00', '2025-02-19'),
(4, 1, '2025-02-19 18:00:00', '2025-02-19'),

(5, 1, '2025-02-19 08:00:00', '2025-02-19'),
(5, 2, '2025-02-19 13:00:00', '2025-02-19'),
(5, 1, '2025-02-19 18:00:00', '2025-02-19'),

(1, 1, '2025-02-20 08:00:00', '2025-02-20'),
(1, 2, '2025-02-20 13:00:00', '2025-02-20'),
(1, 1, '2025-02-20 18:00:00', '2025-02-20'),

(2, 1, '2025-02-20 08:00:00', '2025-02-20'),
(2, 2, '2025-02-20 13:00:00', '2025-02-20'),
(2, 1, '2025-02-20 18:00:00', '2025-02-20'),

(3, 1, '2025-02-20 08:00:00', '2025-02-20'),
(3, 2, '2025-02-20 13:00:00', '2025-02-20'),
(3, 1, '2025-02-20 18:00:00', '2025-02-20'),

(4, 2, '2025-02-20 08:00:00', '2025-02-20'),
(4, 1, '2025-02-20 13:00:00', '2025-02-20'),
(4, 1, '2025-02-20 18:00:00', '2025-02-20'),

(5, 1, '2025-02-20 08:00:00', '2025-02-20'),
(5, 2, '2025-02-20 13:00:00', '2025-02-20'),
(5, 1, '2025-02-20 18:00:00', '2025-02-20'),

(1, 1, '2025-02-21 08:00:00', '2025-02-21'),
(1, 2, '2025-02-21 13:00:00', '2025-02-21'),
(1, 1, '2025-02-21 18:00:00', '2025-02-21'),

(2, 1, '2025-02-21 08:00:00', '2025-02-21'),
(2, 2, '2025-02-21 13:00:00', '2025-02-21'),
(2, 1, '2025-02-21 18:00:00', '2025-02-21'),

(3, 1, '2025-02-21 08:00:00', '2025-02-21'),
(3, 2, '2025-02-21 13:00:00', '2025-02-21'),
(3, 1, '2025-02-21 18:00:00', '2025-02-21'),

(4, 2, '2025-02-21 08:00:00', '2025-02-21'),
(4, 1, '2025-02-21 13:00:00', '2025-02-21'),
(4, 1, '2025-02-21 18:00:00', '2025-02-21'),

(5, 1, '2025-02-21 08:00:00', '2025-02-21'),
(5, 2, '2025-02-21 13:00:00', '2025-02-21'),
(5, 1, '2025-02-21 18:00:00', '2025-02-21'),

(1, 1, '2025-02-22 08:00:00', '2025-02-22'),
(1, 2, '2025-02-22 13:00:00', '2025-02-22'),
(1, 1, '2025-02-22 18:00:00', '2025-02-22'),

(2, 1, '2025-02-22 08:00:00', '2025-02-22'),
(2, 2, '2025-02-22 13:00:00', '2025-02-22'),
(2, 1, '2025-02-22 18:00:00', '2025-02-22'),

(3, 1, '2025-02-22 08:00:00', '2025-02-22'),
(3, 2, '2025-02-22 13:00:00', '2025-02-22'),
(3, 1, '2025-02-22 18:00:00', '2025-02-22'),

(4, 2, '2025-02-22 08:00:00', '2025-02-22'),
(4, 1, '2025-02-22 13:00:00', '2025-02-22'),
(4, 1, '2025-02-22 18:00:00', '2025-02-22'),

(5, 1, '2025-02-22 08:00:00', '2025-02-22'),
(5, 2, '2025-02-22 13:00:00', '2025-02-22'),
(5, 1, '2025-02-22 18:00:00', '2025-02-22'),

(1, 1, '2025-02-23 08:00:00', '2025-02-23'),
(1, 2, '2025-02-23 13:00:00', '2025-02-23'),
(1, 1, '2025-02-23 18:00:00', '2025-02-23'),

(2, 1, '2025-02-23 08:00:00', '2025-02-23'),
(2, 2, '2025-02-23 13:00:00', '2025-02-23'),
(2, 1, '2025-02-23 18:00:00', '2025-02-23'),

(3, 1, '2025-02-23 08:00:00', '2025-02-23'),
(3, 2, '2025-02-23 13:00:00', '2025-02-23'),
(3, 1, '2025-02-23 18:00:00', '2025-02-23'),

(4, 2, '2025-02-23 08:00:00', '2025-02-23'),
(4, 1, '2025-02-23 13:00:00', '2025-02-23'),
(4, 1, '2025-02-23 18:00:00', '2025-02-23'),

(5, 1, '2025-02-23 08:00:00', '2025-02-23'),
(5, 2, '2025-02-23 13:00:00', '2025-02-23'),
(5, 1, '2025-02-23 18:00:00', '2025-02-23');
```

### 테이블 확인

```sql
-- 테이블 구조 확인
DESCRIBE consumption;

-- 테이블 데이터 확인
SELECT * FROM consumption;
```
