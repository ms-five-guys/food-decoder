# 🧠 Azure Custom Vision 이미지 분류 모델

## 📝 개요
- Azure Custom Vision API를 사용하여 Custom Vision Portal에서 생성한 이미지 분류 모델을 호출하여 사용자가 시험하고자 하는 한국 음식 이미지를 분석하고 식품명을 예측하는 프로그램입니다.

## 🚀 주요 기능
- API Key를 사용하여 커스텀 비전 모델 클라이언트 연동
- 구축된 커스텀 비전 모델로 한국 음식 이미지를 분석하고 식품명을 예측

## ⚙️ 환경 설정

1. **필수 요구사항**
- Python 3.9 이상
- Azure Custom Vision subscription

2. **필요한 패키지 설치**
```bash
pip install -r requirements.txt
```

## 📁 프로젝트 구조
```
custom_vision/
│
├── src/               # 소스 코드
├── main.py            # 모델 구축 및 구동
└── README.md          # 문서
```

## 🛠️ 테스트 방법
1. Azure Computer Vision 구독 확인
2. 커스텀 비전 포탈에서 다중 클래스 분류 모델 구축
3. 학습용 이미지 수집 후 모델 학습
4. 학습된 모델을 활성화하여 API 연동에 필요한 값들 생성
5. 이 값들로 클라이언트 인증
6. 테스트용 이미지 수집
7. 수집한 테스트용 이미지를 data 디렉토리에 업로드
8. 테스트용 이미지를 모델에 적용하여 인식 결과 확인

## ⚠️ 주의사항
1. **데이터**
    - 저작권 문제 없는 이미지 사용
    - 한가지의 음식만 나온 한국 음식 이미지 수집
    - 한국 음식 영양성분정보 데이터베이스 불포함
2. **Microsoft Azure**
    - Azure Services 구독 확인