# 🔄 GitHub Actions 배포 가이드

> LinQu 프로젝트의 Azure VM 자동 배포 워크플로우 가이드입니다.

## 1. 📋 워크플로우 개요

- **워크플로우 이름**: Deploy to Azure VM
- **트리거**: main 브랜치에 push 발생 시
- **대상 저장소**: ms-five-guys/food-decoder
- **실행 환경**: Ubuntu Latest

## 2. 🔑 필요한 Secrets

```plaintext
VM_HOST: Azure VM의 IP 주소
VM_USERNAME: VM 사용자 이름
VM_SSH_KEY: SSH 개인키
AZURE_CUSTOM_VISION_ENDPOINT: Custom Vision 엔드포인트
AZURE_CUSTOM_VISION_API_KEY: Custom Vision API 키
AZURE_CUSTOM_VISION_PROJECT_ID: Custom Vision 프로젝트 ID
AZURE_CUSTOM_VISION_MODEL_NAME: Custom Vision 모델 이름
AZURE_MYSQL_HOST: MySQL 서버 주소
AZURE_MYSQL_DATABASE: 데이터베이스 이름
AZURE_MYSQL_USER: 데이터베이스 사용자
AZURE_MYSQL_PASSWORD: 데이터베이스 비밀번호
```

## 3. 🔄 배포 프로세스

### 3.1 파일 복사
```yaml
- name: Copy files to VM
  uses: appleboy/scp-action@master
  with:
    host: ${{ secrets.VM_HOST }}
    username: ${{ secrets.VM_USERNAME }}
    key: ${{ secrets.VM_SSH_KEY }}
    source: "."
    target: "/home/${{ secrets.VM_USERNAME }}/food-classifier"
```

### 3.2 시스템 패키지 설치
- Python 관련: python3-pip, python3-dev, build-essential
- OpenCV 의존성: libgl1, libglib2.0-0, libsm6, libxext6, libxrender-dev
- 기타: debianutils (which 명령어)
- Node.js 20.x

### 3.3 SSL 인증서 설정
- DigiCert Global Root CA 인증서 다운로드
- 권한 설정 (644)

### 3.4 환경 변수 설정
- `/etc/food-classifier/.env` 파일 생성
- Azure 및 데이터베이스 관련 환경 변수 설정

### 3.5 Python 환경 설정
1. 가상환경 생성 또는 재사용
2. pip 업그레이드
3. wheel, setuptools 설치
4. requirements.txt 설치

### 3.6 서비스 재시작
- systemctl을 통한 food-classifier 서비스 재시작

## 4. 🔍 문제 해결 가이드

### 4.1 배포 실패 시 확인사항
1. VM 연결 상태
   - SSH 접속 테스트
   - IP 주소 확인
   - 방화벽 설정 확인

2. 환경 변수
   - GitHub Secrets 설정 확인
   - `.env` 파일 생성 확인
   - 권한 설정 확인

3. 시스템 서비스
   - 서비스 상태 확인: `sudo systemctl status food-classifier`
   - 로그 확인: `sudo journalctl -u food-classifier`

### 4.2 일반적인 오류
```bash
# SSH 연결 확인
ssh -i <key_file> $USERNAME@$VM_HOST

# 서비스 상태 확인
sudo systemctl status food-classifier

# 로그 확인
sudo journalctl -u food-classifier -n 100 --no-pager

# 환경 변수 확인
cat /etc/food-classifier/.env

# 패키지 설치 확인
pip list
```

## 5. 📝 유지보수 가이드

### 5.1 워크플로우 파일 위치
```
.github/workflows/deploy-to-vm.yml
```

### 5.2 보안 고려사항
- Secrets 정기적 업데이트
- SSH 키 관리
- 환경 변수 파일 권한 관리
- SSL 인증서 유효기간 관리

## 6. 📚 참고 자료
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [GitHub Secrets 설정 가이드](https://docs.github.com/en/actions/security-guides/encrypted-secrets)