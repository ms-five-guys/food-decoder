# 🎨 식단 관리 서비스 UI 아키텍처

## 1. 📱 서비스 개요

### 1.1 주요 기능
- 고객 정보 조회 및 관리
- 음식 이미지 분석
- 영양 정보 추적 및 시각화
- 실시간 섭취량 모니터링

### 1.2 기술 스택
- UI: Python with Gradio

## 2. 🏗️ UI 구조

### 2.1 디렉터리 구조
```
service_ui/
├── app.py                 # 메인 애플리케이션
├── communicators/         # 외부 시스템 통신 모듈
├── pages/                 # UI 페이지 모듈
└── processors/            # 데이터 처리 모듈
```

### 2.2 주요 모듈
1. **외부 시스템 연동 모듈**
   - `MLCommunicator`: Azure Custom Vision 연동
   - `DBCommunicator`: Azure Database for MySQL Flexible Server 연동

2. **페이지 모듈**
   - `CustomerPage`: 고객 정보 관리 화면
   - `NutritionPage`: 영양 정보 관리 화면

3. **데이터 처리 모듈**
   - `CustomerProcessor`: 고객 정보 처리 및 시각화
   - `FoodProcessor`: 음식 이미지 분석 및 영양 정보 처리
   - `CustomerSession`: 고객 세션 관리
   - `NutritionUtils`: 영양 정보 표시 및 계산

### 2.3 모듈 구성도

```mermaid
graph TD
    subgraph " 📱 Pages "
        CP[CustomerPage]
        NP[NutritionPage]
    end

    subgraph " ⚙️ Processors "
        CProc[CustomerProcessor]
        FProc[FoodProcessor]
        CS[CustomerSession]
        NU[NutritionUtils]
    end

    subgraph " 🔌 Communicators "
        MLC[MachineLearningCommunicator]
        DBC[DatabaseCommunicator]
    end

    subgraph " 🌐 External Systems "
        CV[Azure Custom Vision]
        DB[(MySQL Database)]
    end

    %% Pages -> Processors
    CP --> CProc
    CP --> CS
    NP --> FProc
    NP --> NU

    %% Processors -> Communicators
    FProc --> MLC
    FProc --> DBC
    CProc --> DBC
    CS --> DBC

    %% Communicators -> External
    MLC --> CV
    DBC --> DB

    %% 스타일링
    classDef page fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef processor fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#000
    classDef external fill:#fafafa,stroke:#424242,stroke-width:2px,color:#000
    classDef communicator fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef default fontSize:12px
    %% subgraph 스타일링
    classDef subgraphStyle fill:none,stroke-dasharray: 5 5

    class CP,NP page
    class CProc,FProc,CS,NU processor
    class MLC,DBC communicator
    class CV,DB external
```

## 3. ✨ 페이지별 주요 기능

### 3.1 고객 정보 페이지
- 고객/보호자 코드 기반 로그인
- 고객 프로필 표시
  - 기본 정보 (이름, 나이, 성별 등)
- 영양 섭취 요약 대시보드

### 3.2 영양 관리 페이지
- 음식 이미지 분석 기능
  - 실시간 이미지 업로드
  - AI 기반 음식 분류
  - 영양 성분 자동 계산
- 섭취량 모니터링
  - 일일 권장량 대비 현재 섭취량
  - 과다 섭취 시 경고 알림

## 4. 📊 시각화 컴포넌트

### 4.1 영양 섭취 그래프
- 최근 5일 섭취 트렌드
  - 일별 주요 영양소 섭취량
  - 권장 섭취량 범위 표시
- 영양소별 섭취 현황
  - 과다/과소 섭취 경고
  - 권장 섭취 구간 표시

### 4.2 실시간 모니터링
- 일일 섭취량 진행바
  - 영양소별 색상 구분
  - 실시간 업데이트
- 경고 알림 시스템
  - 과다 섭취 경고

## 📊 5. System Interaction Flow
이 섹션은 `service_ui` 모듈을 통해 사용자와 시스템 간의 상호작용을 두 가지 주요 흐름으로 설명합니다. 첫 번째 흐름은 고객 정보와 최근 영양 성분 섭취 정보를 조회하는 과정이며, 두 번째 흐름은 이미지를 처리하여 영양 정보를 제공하는 과정입니다.

### 5.1 고객 정보 조회 (Customer Information Retrieval)
이 다이어그램은 사용자가 Gradio UI를 통해 고객 코드와 보호자 코드를 입력하여 데이터베이스에서 고객 정보와 최근 5일치 영양 성분 섭취 정보를 조회하는 과정을 설명합니다. 조회된 정보는 사용자에게 표시됩니다.

```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#E8F5E9',
      'primaryTextColor': '#1b5e20',
      'primaryBorderColor': '#90EE90',
      'lineColor': '#2e7d32',
      'secondaryColor': '#E8F5E9',
      'tertiaryColor': '#FFFFFF',
      'noteTextColor': '#1b5e20',
      'noteBorderColor': '#2e7d32',
      'noteBkgColor': '#E8F5E9',
      'actorTextColor': '#1b5e20',
      'actorBorder': '#2e7d32',
      'actorBkg': '#E8F5E9'
    }
  }
}%%

sequenceDiagram
    title 고객 정보 및 영양 정보 조회 과정
    actor 사용자
    participant UI as 📱 Gradio UI
    participant VM as ☁️ Azure VM
    participant DB as 🗃️ Azure MySQL
    
    사용자->>UI: 서비스 접속
    UI->>사용자: 코드 입력 요청
    Note over 사용자,UI: 고객 코드 &<br/>보호자 코드
    사용자->>UI: 두 코드 입력
    UI->>VM: 코드 전송
    Note over VM: 코드 조합
    VM->>DB: 고객 정보와 최근 영양 정보 조회
    Note over DB: 일치하는 고객 정보 확인
    DB->>VM: 고객 정보와 최근 영양 정보 반환
    
    VM->>UI: 고객 정보와 최근 영양 정보 표시
    UI->>사용자: 고객 정보와 최근 영양 정보 확인
```

### 5.2 영양 정보 분석 (Nutrition Information Analysis)
이 다이어그램은 사용자가 음식 이미지를 제출하면 영양 정보를 분석하고 표시하는 과정을 설명합니다. 사용자는 카메라로 촬영하거나 갤러리에서 이미지를 선택할 수 있으며, Custom Vision이 음식을 식별합니다. 분석된 결과는 일일 권장 영양소 대비 섭취량을 막대 그래프로 시각화하고, 오늘 섭취한 음식 기록을 함께 표시합니다.

```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#E8F5E9',
      'primaryTextColor': '#1b5e20',
      'primaryBorderColor': '#90EE90',
      'lineColor': '#2e7d32',
      'secondaryColor': '#E8F5E9',
      'tertiaryColor': '#FFFFFF',
      'noteTextColor': '#1b5e20',
      'noteBorderColor': '#2e7d32',
      'noteBkgColor': '#E8F5E9',
      'actorTextColor': '#1b5e20',
      'actorBorder': '#2e7d32',
      'actorBkg': '#E8F5E9'
    }
  }
}%%

sequenceDiagram
    title 이미지 처리 및 영양 정보 분석 과정
    actor 사용자
    participant UI as 📱 Gradio UI
    participant VM as ☁️ Azure VM
    participant ML as 🧠 Custom Vision
    participant DB as 🗃️ Azure MySQL
    
    UI->>사용자: 이미지 입력 옵션 표시
    Note over 사용자,UI: 카메라 또는<br/>갤러리 업로드
    
    alt 카메라
        사용자->>UI: 사진 촬영
    else 갤러리
        사용자->>UI: 이미지 업로드
    end
    
    UI->>VM: 이미지 전송
    VM->>ML: 예측 요청
    Note over ML: 이미지 처리<br/>음식 분류
    
    ML->>VM: 음식 이름과 신뢰도 반환
    Note over ML,VM: 신뢰도 점수와 함께<br/>음식 분류 결과
    
    VM->>DB: 권장 섭취량 정보 조회
    VM->>UI: 고객 정보가 없을 경우<br/>메시지 생성
    Note over UI: 고객 정보가 없을 경우<br/>메시지 표시
    DB->>VM: 권장 섭취량 반환
    Note over VM: 권장 섭취량<br/>기준 확인
    
    VM->>DB: 오늘 섭취한 음식 정보 조회
    VM->>UI: 고객 정보가 없을 경우<br/>메시지 생성
    Note over UI: 고객 정보가 없을 경우<br/>메시지 표시
    DB->>VM: 오늘의 섭취 기록 반환
    Note over VM: 현재 섭취량<br/>합산 계산
    
    VM->>DB: 타임스탬프와 함께 음식 섭취 기록
    VM->>UI: 고객 정보가 없을 경우<br/>메시지 생성
    Note over UI: 고객 정보가 없을 경우<br/>메시지 표시
    Note over DB: 음식 ID와<br/>섭취 시간 기록
    VM->>DB: 음식 이름으로 영양 정보 조회
    Note over DB: 일치하는 영양 정보 확인
    
    DB->>VM: 영양 정보 반환
    
    VM->>UI: 결과 형식화
    Note over UI: 초과 영양소가 있는 경우<br/>경고 메시지 표시
    UI->>사용자: 영양 정보와 신뢰도 표시
```