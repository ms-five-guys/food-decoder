# <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&pause=1000&color=FFFFFF&center=true&vCenter=true&repeat=false&random=false&width=65&height=40&lines=Lin" alt="Lin" style="background-color: #E8F5E9;"/><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&pause=1000&color=90EE90&center=true&vCenter=true&repeat=false&random=false&width=55&height=40&lines=Qu" alt="Qu" style="background-color: #E8F5E9;"/> 

> 🍽️ 시니어 대상 음식 이미지 인식 서비스 (Link you) LinQu

## 🌐 Service Information
| Type | URL | Status |
|------|-----|--------|
| Production | [nutricare.koreacentral.cloudapp.azure.com](https://nutricare.koreacentral.cloudapp.azure.com/) | 🔴 Deactivated |

> **Note**: 서비스 문제 발생 시 [이슈](https://github.com/ms-five-guys/food-decoder/issues)를 생성해주세요.

## 👥 Team Five Guys
- 김기덕 [@GideokKim](https://github.com/GideokKim)
- 이희주 [@YiHeeJu](https://github.com/YiHeeJu)
- 윤소영 [@Yoonsoyoung02](https://github.com/Yoonsoyoung02)
- 박현열 [@yoplnaa](https://github.com/yoplnaa)
- 김민석 [@BrianK64](https://github.com/BrianK64)

## 📝 프로젝트 개요
Azure Custom Vision과 Azure Database for MySQL Flexible Server, Gradio를 활용한 시니어 대상 음식 이미지 인식 서비스입니다.

### 🎯 주요 기능
- 실시간 음식 이미지 인식 및 분류
- 개인별 영양 섭취 기록 관리
- 맞춤형 영양 정보 제공
- 일일/주간 영양 섭취 분석

## 🛠️ Tech Stack

### 🎨 Interface
- 🖥️ Gradio (Python UI Library)
- 📊 Matplotlib (Data Visualization)
- 📸 OpenCV (Image Processing)

### 🧠 AI/ML
- 🧠 [Azure Custom Vision](https://learn.microsoft.com/ko-kr/azure/cognitive-services/custom-vision-service/) (ML Model)
- 🔮 CNN Architecture
- 🎯 ResNet50 (Deep Learning Model)
- 🎨 Stable-diffusion (Image Generation)

### ☁️ Cloud Infrastructure
- ☁️ [Azure VM](https://learn.microsoft.com/ko-kr/azure/virtual-machines/) (Cloud Computing)
- 🗃️ [Azure Database for MySQL Flexible Server](https://learn.microsoft.com/ko-kr/azure/mysql/flexible-server/)

### 🚀 Deployment
- 🔄 GitHub Actions (Continuous Deployment)
- 🔐 GitHub Secrets (Secret Management)

### 🔨 Development Tools
- 🐍 Python 3.9+
- 📓 Jupyter Notebook
- 📝 Git (Version Control)
- 😜 [Gitmoji](https://gitmoji.dev/) (Commit Convention)

## 📊 System Interaction Flow
이 섹션은 사용자와 시스템 간의 상호작용을 설명합니다. 자세한 시스템 흐름도와 설명은 [서비스 UI 아키텍처 문서](docs/service-ui-architecture.md#-5-system-interaction-flow)를 참조하세요.

주요 상호작용:
1. 고객 정보 조회 (Customer Information Retrieval)
   - 고객/보호자 코드 기반 인증
   - 최근 5일 영양 섭취 정보 조회

2. 영양 정보 분석 (Nutrition Information Analysis)
   - 이미지 기반 음식 분류
   - 실시간 영양 정보 분석
   - 섭취량 모니터링 및 경고

## 🤝 Contributing
프로젝트 기여 방법은 [CONTRIBUTING.md](.github/CONTRIBUTING.md)를 참고해주세요.

## 📞 Support
[이슈](https://github.com/ms-five-guys/food-decoder/issues)를 생성해주세요.
