## 🤝 기여하기

### 🔄 Fork 및 Clone 설정
1. GitHub에서 프로젝트를 Fork 합니다.
2. Fork한 저장소를 로컬에 Clone 합니다:
```bash
git clone git@github.com:your-username/your-repository.git
cd your-repository
```

### 🔗 Upstream 설정
3. 원본 저장소를 upstream으로 등록합니다:
```bash
# upstream 저장소 추가
git remote add upstream git@github.com:ms-five-guys/food-decoder.git

# 설정된 remote 저장소 확인
git remote -v
```

### ⚙️ 환경 설정
4. **가상환경 설정**
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

5. **필요한 패키지 설치**
```bash
pip install -r requirements.txt
```

### 🔄 브랜치 동기화
6. 원본 저장소의 최신 변경사항을 가져옵니다:
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

### ✨ 기능 개발
7. 새로운 기능 브랜치 생성:
```bash
git checkout -b feature/your-feature-name
```

8. 변경사항 커밋:
```bash
git add .
gitmoji -c
git push origin feature/your-feature-name
```

9. GitHub에서 Pull Request 생성

### ⚠️ 주의사항
- PR 생성 전에 항상 upstream의 최신 변경사항을 동기화해주세요
- 하나의 PR에는 하나의 기능/수정만 담아주세요
- 커밋 메시지는 명확하게 작성해주세요 