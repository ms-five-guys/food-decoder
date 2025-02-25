# 🔄 Azure VM과 GitHub Actions 연동 가이드

이 가이드는 GitHub Actions를 사용하여 Azure VM에 지속적 배포를 설정하는 방법을 설명합니다.

## 🔧 사전 요구사항

- 활성 구독이 있는 Azure 계정
- GitHub 저장소
- Ubuntu가 실행되는 Azure VM
- VM에 대한 SSH 접근 권한

## 1. 🖥️ Azure VM 설정

> 이미 Azure VM Resource를 생성하였다고 가정합니다.

### 1.1 SSH 키 쌍 생성 및 설정

1. **SSH 키 쌍 생성**
```bash
# SSH 키 쌍 생성
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 생성된 키 확인
ls -la ~/.ssh/
# id_rsa (개인키)
# id_rsa.pub (공개키)
```

2. **Azure VM에 공개키 설정**
```bash
# 공개키 내용을 클립보드에 복사
# macOS
cat ~/.ssh/id_rsa.pub | pbcopy

# Windows (PowerShell)
Get-Content ~/.ssh/id_rsa.pub | Set-Clipboard

# Linux
cat ~/.ssh/id_rsa.pub | xclip -selection clipboard
```
- VM에 SSH 접속: `ssh azureuser@VM_IP_ADDRESS`
- `~/.ssh/authorized_keys` 파일 열기: `vim ~/.ssh/authorized_keys`
- 클립보드 내용 붙여넣기
- 파일 권한 설정: `chmod 600 ~/.ssh/authorized_keys`

3. **GitHub Secrets 설정**
```bash
# 개인키 내용을 클립보드에 복사
# macOS
cat ~/.ssh/id_rsa | pbcopy

# Windows (PowerShell)
Get-Content ~/.ssh/id_rsa | Set-Clipboard

# Linux
cat ~/.ssh/id_rsa | xclip -selection clipboard
```
- GitHub 저장소 → Settings → Secrets and variables → Actions
- New repository secret 클릭
- 다음 secrets 추가:
  ```
  VM_HOST: Azure VM의 IP 주소
  VM_USERNAME: VM 사용자 이름 (보통 'azureuser')
  VM_SSH_KEY: 클립보드에 복사한 개인키 내용 붙여넣기
  ```

4. **연결 테스트**
```bash
# VM SSH 연결
ssh -i 최초 발급 받은 vm 개인키.pem azureuser@VM_IP_ADDRESS
```

주의사항:
- 개인키(`id_rsa`)는 절대 공개되면 안 됨
- GitHub Secrets에 등록한 개인키는 마스킹 처리되어 로그에 노출되지 않음
- VM의 `authorized_keys` 파일 권한은 600으로 설정
- `.ssh` 디렉토리 권한은 700으로 설정

### 1.2 네트워크 보안 구성
1. Azure 포털 → VM → 네트워킹으로 이동
2. 인바운드 포트 규칙 추가:
   - SSH (22)
   - 애플리케이션 포트 (Gradio용 7860)

## 2. 📦 GitHub 저장소 구성

### 2.1 GitHub Secrets 추가
저장소 Settings → Secrets and variables → Actions에서 추가:
- `VM_HOST`: VM의 공개 IP 주소
- `VM_USERNAME`: VM 사용자 이름 (보통 'azureuser')
- `VM_SSH_KEY`: 개인 SSH 키 내용

### 2.2 GitHub Actions 워크플로우 생성

`.github/workflows/deploy-to-vm.yml` 파일을 생성하고 다음 내용을 추가합니다:

```yaml
name: Deploy to Azure VM

on:
  push:
    branches:
      - main  # main 브랜치 push 시에만 실행

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2  # Checkout repository code
      
      - name: Copy files to VM
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.VM_HOST }}  # VM's IP address
          username: ${{ secrets.VM_USERNAME }}  # VM username
          key: ${{ secrets.VM_SSH_KEY }}  # SSH private key
          source: "."  # Source directory to copy
          target: "/home/${{ secrets.VM_USERNAME }}/food-classifier"  # Target directory on VM
```

워크플로우 파일의 각 섹션 설명:

1. **기본 설정**
   - `name`: 워크플로우의 이름
   - `on.push.branches`: main 브랜치에 push될 때만 실행

2. **작업 환경**
   - `runs-on`: Ubuntu 최신 버전에서 실행
   - `steps`: 순차적으로 실행할 작업들

3. **코드 체크아웃**
   - `actions/checkout@v2`: 저장소 코드를 가져옴

4. **파일 복사**
   - `appleboy/scp-action`: SCP를 사용해 파일을 VM으로 복사
   - `host`: VM의 IP 주소
   - `username`: VM 사용자 이름
   - `key`: SSH 개인키
   - `source`: 복사할 소스 디렉토리
   - `target`: VM의 대상 디렉토리

5. **배포 스크립트**
   ```yaml
   - name: Deploy to VM
     uses: appleboy/ssh-action@master
     with:
       host: ${{ secrets.VM_HOST }}
       username: ${{ secrets.VM_USERNAME }}
       key: ${{ secrets.VM_SSH_KEY }}
       script: |
         # 시스템 패키지 설치
         sudo apt-get update
         sudo apt-get install -y python3-pip python3-dev build-essential
         
         # Node.js 설치
         curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
         sudo apt-get install -y nodejs
         
         # 환경 변수 설정
         cat > /etc/food-classifier/.env << 'EOL'
         AZURE_CUSTOM_VISION_ENDPOINT="${{ secrets.AZURE_CUSTOM_VISION_ENDPOINT }}"
         AZURE_CUSTOM_VISION_API_KEY="${{ secrets.AZURE_CUSTOM_VISION_API_KEY }}"
         AZURE_CUSTOM_VISION_PROJECT_ID="${{ secrets.AZURE_CUSTOM_VISION_PROJECT_ID }}"
         AZURE_CUSTOM_VISION_MODEL_NAME="${{ secrets.AZURE_CUSTOM_VISION_MODEL_NAME }}"
         EOL
         
         # Python 환경 설정
         cd ~/food-classifier
         if [ ! -d "venv" ]; then
             python3 -m venv venv
         fi
         source venv/bin/activate
         pip install -r requirements.txt
         
         # 서비스 재시작
         sudo systemctl restart food-classifier
   ```

배포 스크립트 단계별 설명:
1. **시스템 패키지**: 필요한 시스템 패키지들을 설치
2. **Node.js**: Gradio 웹 인터페이스에 필요한 Node.js 설치
3. **환경 변수**: Azure Custom Vision API 접근을 위한 환경 변수 설정
4. **Python 환경**: 가상환경 설정 및 패키지 설치
5. **서비스**: 애플리케이션 서비스 재시작

이 워크플로우는 코드가 main 브랜치에 병합될 때마다 자동으로 실행되어 VM에 최신 코드를 배포합니다.

## 3. 🛠️ 서비스 구성

### 3.1 Systemd 서비스 생성
```bash
sudo vim /etc/systemd/system/food-classifier.service
```

다음 내용 추가:
```ini
[Unit]
Description=Food Classifier Gradio App
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/food-classifier/food_classifier/src/service_ui
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
Environment=PYTHONPATH=/home/azureuser/food-classifier
EnvironmentFile=/etc/food-classifier/.env
ExecStart=/home/azureuser/food-classifier/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3.2 서비스 관리 명령어
```bash
# systemd 데몬 리로드
sudo systemctl daemon-reload

# 서비스 시작
sudo systemctl start food-classifier

# 서비스 상태 확인
sudo systemctl status food-classifier

# 서비스 중지
sudo systemctl stop food-classifier
```

## 4. ⚙️ 환경 변수

`/etc/food-classifier/`에 `.env` 파일 생성:
```bash
AZURE_CUSTOM_VISION_ENDPOINT="your_endpoint"
AZURE_CUSTOM_VISION_API_KEY="your_key"
AZURE_CUSTOM_VISION_PROJECT_ID="your_project_id"
AZURE_CUSTOM_VISION_MODEL_NAME="your_model_name"
```

## 5. 💰 비용 관리

### 5.1 자동 종료 구성
1. Azure 포털 → VM → 작업 → 자동 종료로 이동
2. 원하는 종료 시간 설정
3. 선택사항: 이메일 알림 구성

### 5.2 수동 VM 관리
```bash
# VM 중지
az vm stop --resource-group myResourceGroup --name myVM

# VM 시작
az vm start --resource-group myResourceGroup --name myVM
```

## 6. 🔍 문제 해결

### 6.1 서비스 로그 확인
```bash
# 실시간 로그 보기
sudo journalctl -u food-classifier -f

# 최근 로그 보기
sudo journalctl -u food-classifier -n 50
```

### 6.2 일반적인 문제
1. 서비스 시작 실패:
   - journalctl로 로그 확인
   - 환경 변수 확인
   - Python 의존성 확인

2. 웹 인터페이스 접속 불가:
   - 서비스 실행 여부 확인
   - Azure NSG에서 포트 7860 개방 확인
   - VM 실행 여부 확인

## 7. 🔄 유지보수

### 7.1 의존성 업데이트
```bash
cd ~/food-classifier
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### 7.2 시스템 업데이트
```bash
sudo apt update
sudo apt upgrade
```

## 8. 🔒 보안 고려사항

1. SSH 키 안전하게 보관
2. 시스템 패키지 정기적 업데이트
3. 강력한 비밀번호 사용
4. VM 접근 로그 모니터링
5. 방화벽 규칙 적절히 구성

## 9. 📚 추가 자료

- [Azure VM 문서](https://docs.microsoft.com/azure/virtual-machines/)
- [GitHub Actions 문서](https://docs.github.com/actions)
- [Gradio 문서](https://gradio.app/docs/)