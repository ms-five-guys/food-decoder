# 🖥️ Azure VM 설정 가이드

## 1. 🚀 Azure 리소스 생성

### 1.1 Azure 구독 및 리소스 그룹

1. Azure Portal(https://portal.azure.com)에 로그인
2. 리소스 그룹 생성
   - 상단 검색창에서 "리소스 그룹" 검색
   - "만들기" 클릭
   - 이름: `linqu-vm-rg`
   - 지역: `Korea Central`

### 1.2 Virtual Machine 생성

1. "가상 머신" 검색 후 "만들기" 클릭
2. 기본 사항:
   - 이름: `linqu-vm`
   - 지역: `Korea Central`
   - 이미지: `Ubuntu Server 24.04 LTS`
   - 크기: `Standard DS1 v2` (1vCPU, 3.5GiB memory)
3. 관리자 계정:
   - 인증 유형: `SSH 공개 키`
   - 사용자 이름: `azureuser`
   - SSH 공개 키 소스: `새 키 쌍 생성`
4. 네트워킹:
   - 가상 네트워크: 이전에 생성한 VNet 선택
   - 공용 IP: `새로 만들기`
   - HTTP(80), HTTPS(443) 포트 허용

## 2. 🛠️ VM 초기 설정

### 2.1 SSH 접속

```bash
# SSH 접속(SSH 키 파일 경로 지정)
ssh -i your-key.pem azureuser@YOUR_VM_IP
```

### 2.2 기본 패키지 설치

```bash
# 시스템 업데이트
sudo apt update
sudo apt upgrade -y

# 기본 도구 설치
sudo apt install -y build-essential git curl
```

## 3. 🔍 모니터링 및 유지보수

### 3.1 로그 확인

```bash
# 시스템 로그 확인
sudo tail -f /var/log/syslog

# 서비스 로그 확인
tail -f /app/logs/application.log
```

### 3.2 시스템 모니터링

```bash
# 디스크 사용량 확인
df -h

# 메모리 사용량 확인
free -h

# CPU 사용량 확인
top
```

### 3.3 백업 (선택사항)

- 중요 데이터는 주기적으로 백업
- Azure Backup 서비스 사용 고려
- 서비스 설정 파일 백업

## 4. 🔒 보안 권장사항

1. 정기적인 보안 업데이트 적용
2. SSH 키 기반 인증만 허용
3. 필요한 포트만 개방
4. 로그 모니터링 설정

## 5. 🔧 문제 해결

1. SSH 연결 실패
   - 보안 그룹 규칙 확인
   - SSH 키 권한 확인 (400)
   - 네트워크 인터페이스 상태 확인

2. 디스크 공간 부족
   - 불필요한 로그 파일 정리
   - 디스크 확장 고려

3. 성능 이슈
   - VM 크기 조정 고려
   - 리소스 사용량 모니터링
   - 서비스 메모리 누수 확인

4. 서비스 장애
   - 시스템 리소스 사용량 확인
   - 서비스 로그 분석 