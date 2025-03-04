# Azure Custom Vision Classification

## 개요
이 문서는 Azure Custom Vision API를 사용하여 음식 이미지를 분류하는 방법을 설명합니다. 이 프로젝트는 Python을 사용하여 Azure의 Custom Vision 모델을 호출하고, 예측 결과를 시각화하며, 영양 정보를 추출하는 과정을 포함합니다.

## 라이브러리 설치
필요한 라이브러리를 설치합니다.
```bash
pip install azure-cognitiveservices-vision-customvision
pip install python-dotenv
pip install matplotlib
pip install pandas
```

## 환경 설정
환경변수에서 API 관련 정보를 불러와서 클라이언트를 인증합니다.

```python
from config import get_config

config = get_config()
ENDPOINT = config["ENDPOINT"]
KEY = config["KEY"]
PROJECT_ID = config["PROJECT_ID"]
MODEL_NAME = config["MODEL_NAME"]
```

## 이미지 분류
테스트 이미지를 Custom Vision 모델에 적용하여 결과를 얻습니다.

```python
from PIL import Image
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import CognitiveServicesCredentials

# 클라이언트 인증
credentials = CognitiveServicesCredentials(KEY)
classifier = CustomVisionPredictionClient(endpoint=ENDPOINT, credentials=credentials)

# 이미지 파일 열기
image_file = "gimbap.png"
with open(image_file, mode="rb") as image_data:
    results = classifier.classify_image(PROJECT_ID, MODEL_NAME, image_data)

# 예측 결과 출력
for prediction in results.predictions:
    print(f"음식: {prediction.tag_name}\t\t Probability: {prediction.probability:.2f}")
```

## 영양 정보 추출
예측된 음식에 대한 영양 정보를 CSV 파일에서 추출합니다.

```python
import pandas as pd

# CSV 파일 읽기
food_db = pd.read_csv("sample_database.csv", encoding="cp949")

# 예측된 음식의 영양 정보 출력
food_label = results.predictions[0].tag_name
nutrition = food_db.loc[food_db["식품명"] == food_label]
print(nutrition)
```

## 결론
이 프로젝트는 Azure Custom Vision API를 사용하여 이미지 분류를 수행하고, 예측된 음식에 대한 영양 정보를 추출하는 방법을 보여줍니다.
