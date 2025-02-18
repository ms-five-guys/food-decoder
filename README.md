# 🧠 CNN 기반 실시간 음식 인식 프로젝트

## 📝 프로젝트 개요
- CNN 기반 음식 인식 모델을 개발하여 실시간으로 음식을 분석하고 영양 성분 정보를 제공하는 시스템
- Azure를 활용한 클라우드 기반 서비스 구축
- Git을 통한 버전 관리 및 협업

## 🚀 시작하기

### 필수 요구사항
- Python 3.9 이상
- pip (Python 패키지 관리자)
- Git

### ⚙️ 환경 설정

1. **저장소 클론**
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

2. **가상환경 설정**
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **필요한 패키지 설치**
```bash
pip install -r requirements.txt
```

## 📁 프로젝트 구조
```
project/
│
├── data/               # 데이터셋 저장소
├── models/            # 학습된 모델 파일
├── src/               # 소스 코드
├── tools/             # 유틸리티 스크립트
├── requirements.txt   # 프로젝트 의존성
└── README.md         # 프로젝트 문서
```

## 🛠️ 주요 기능
- 실시간 음식 이미지 인식
- 영양 성분 정보 제공
- 데이터베이스 검색 및 관리

## 📚 참고 자료
- [프로젝트 위키](https://github.com/ms-five-guys/food-decoder/wiki)
- [문제 해결 가이드](https://github.com/ms-five-guys/food-decoder/wiki)

## 🤝 기여하기

### Fork 및 Clone 설정
1. GitHub에서 프로젝트를 Fork 합니다.
2. Fork한 저장소를 로컬에 Clone 합니다:
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Upstream 설정
3. 원본 저장소를 upstream으로 등록합니다:
```bash
# upstream 저장소 추가
git remote add upstream git@github.com:ms-five-guys/food-decoder.git

# 설정된 remote 저장소 확인
git remote -v
```

### 브랜치 동기화
4. 원본 저장소의 최신 변경사항을 가져옵니다:
```bash
# upstream의 변경사항 가져오기
git fetch upstream

# 로컬 main 브랜치로 이동
git checkout main

# upstream의 변경사항을 로컬 main에 병합
git merge upstream/main

# 변경사항을 fork한 저장소에 반영
git push origin main
```

### 기능 개발
5. 새로운 기능 브랜치 생성:
```bash
git checkout -b feature/your-feature-name
```

6. 변경사항 커밋:
```bash
git add .
gitmoji -c
git push origin feature/your-feature-name
```

7. GitHub에서 Pull Request 생성

### 주의사항
- PR 생성 전에 항상 upstream의 최신 변경사항을 동기화해주세요
- 하나의 PR에는 하나의 기능/수정만 담아주세요
- 커밋 메시지는 명확하게 작성해주세요

## 📝 라이선스
이 프로젝트는 [라이선스명] 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

## ✨ 팀원
- 김기덕 - [GitHub](https://github.com/GideokKim)
- 이희주 - [GitHub](https://github.com/YiHeeJu)
- 윤소영 - [GitHub](https://github.com/Yoonsoyoung02)
- 박현열 - [GitHub](https://github.com/yoplnaa)
- 김민석 - [GitHub](https://github.com/BrianK64)
