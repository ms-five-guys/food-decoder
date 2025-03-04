# azure_cv_classification_v1.py

# Azure 커스텀 비전 API 호출을 통해서 모델을 서비스 제작에 활용

# 라이브러리 등록
# pip install azure-cognitiveservices-vision-customvision
# pip install python-dotenv

# Matplotlib의 pyplot을 사용하여 예측 결과를 그리기
from matplotlib import pyplot as plt

# Python Image 라이브러리로 이미지 불러오기
from PIL import Image

# Custom Vision에 있는 값을 지정하여 클라이언트 인증
# 보완성을 위해 환경변수에서 API 관련 정보를 불러와서 endpoint, key 등을 지정해주고 클라이언트 연동해주는 함수들 불러오기
from config import *

# 커스텀 비전 포탈에서 만든 음식 이미지 분류 모델의 endpoint, key, project id, model name 지정
# config에 포함되어있는 get_config() 함수를 이용하여 환경변수에서 모델의 endpoint, key, project_id, 그리고 model_name을 불러오기
config = get_config()

ENDPOINT = config["ENDPOINT"]
KEY = config["KEY"]
PROJECT_ID = config["PROJECT_ID"]
MODEL_NAME = config["MODEL_NAME"]

# 커스텀 비전 모델을 사용할 클라이언트 인증
# 지정한 API KEY를 써서 커스텀 비전 모델을 사용할 클라이언트를 인증
from msrest.authentication import CognitiveServicesCredentials
credentials = CognitiveServicesCredentials(KEY)
# ENDPOINT를 써서 클라이언트 등록
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
classifier = CustomVisionPredictionClient(endpoint=ENDPOINT, credentials=credentials)

# 분류할 이미지 읽기
# 테스트용으로 사용된 이미지는 AI-Hub 에서 데이터 다운로드 허가 승인을 받은 **한국 이미지(음식)** 데이터셋에 포함되어있는 김밥 이미지.
# 개인 테스트용으로는 Kaggle이나 AI-Hub에 자동승인 또는 샘플 데이터 이용 권장.
# 테스트 이미지 경로 지정
image_file = "gimbap.png"
# 테스트용 이미지 파일 불러오기
image = Image.open(image_file)

# 테스트용 이미지를 커스텀 비전 모델에 적용하여 결과 얻기
# 테스트 이미지를 열고 모델에 적용해서 결과를 저장
with open(image_file, mode="rb") as image_data:
    results = classifier.classify_image(PROJECT_ID, MODEL_NAME, image_data)

# 예측한 결과를 모두 출력 (텍스트로 표시됨)
for prediction in results.predictions:
    print(f"음식: {prediction.tag_name}\t\t Probability: {prediction.probability:.2f}")

# 커스텀 비전 모델이 예측한 결과들이 확률 높은 순서로 **list**형식으로 저장되어있음
# 가장 높은 확률의 예측값만 필요하기 때문데 인덱스 0을 써서 이 값만 추출
# 분류 결과들중 확률이 가장 높게 나온 태그 값 하나만 출력
# 테스트 이미지를 열고 모델에 적용해서 결과를 저장
with open(image_file, mode="rb") as image_data:
    results = classifier.classify_image(PROJECT_ID, MODEL_NAME, image_data)

plt.imshow(image)

# 예측한 결과들중 확률이 가장 높게 나온 결과의 태그와 확률을 변수로 각각 지정
prediction = results.predictions[0]
food_label = prediction.tag_name
prob = prediction.probability

print(f"음식: {food_label}\t\t Probability: {prob * 100:.2f}%")

# 음식종류별 영양성분정보가 표시되어있는 csv 파일을 이용해 커스텀 비전 모델이 예측한 음식에 대한 영양정보 추출
# Imports
# 데이터셋과 작업하기 위해 필요한 라이브러리
import pandas as pd

# csv파일을 pandas 데이터프레임으로 저장
food_db = pd.read_csv("sample_database.csv", encoding="cp949")

# 데이터프레임 확인
food_db.head()

# encoding을 cp949, utf-8-sig, euc-kr로 지정해서 데이터프레임을 불러와봤지만 특정 문자나 단어가 "?"로 표시되어 새로운 데이터 프레임을 직접 생성
# Python 딕셔너리로부터 pandas 데이터프레임 생성
# 각 음식에 대한 에너지, 수분, 단백질, 지방, 탄수화물, 그리고 당류는 정확한 정보 없이 테스트를 위해 임의로 지정한 값들이기때문에 실제 이용시 값 조정 또는 위 방법으로 개인의 데이터셋 사용 필요.
nutrition_facts = {
    "식품명": ["김치찌개", "떡볶이", "김밥"],
    "에너지(kcal)": [19, 130, 157],
    "수분(g)": [33.3, 52.7, 27.1],
    "단백질(g)": [1.2, 3.2, 4.7],
    "지방(g)": [0.53, 1.3, 1.83],
    "탄수화물(g)": [2.33, 27.18, 29.79],
    "당류(g)": [0.94, 4.43, 0.69]
}

# 딕셔너리를 pandas 데이터프레임으로 변환
temp = pd.DataFrame(nutrition_facts)

# 생성된 데이터 프레임 확인
temp.head()

# 커스텀 비전 분류 데모
# 총 3가지의 음식 종류의 각 3개의 이미지를 커스텀 비전 모델을 아용하여 음식 종류를 예측하고, 예측한 값으로 데이터베이스에서 영양정보를 추출해내는 과정 데모
# 테스트용으로 사용된 이미지들은 AI-Hub 에서 데이터 다운로드 허가 승인을 받은 **한국 이미지(음식)** 데이터셋에 포함되어있는 이미지들.
# 개인 테스트용으로는 Kaggle이나 AI-Hub에 자동승인 또는 샘플 데이터 이용 권장.
import time

# 로컬에 저장된 샘플 이미지 경로들 리스트에 저장하기
# 사용된 이미지 통계
# 음식 종류: 김치찌개, 떡볶이, 김밥
# 이미지수: 각 종류별 3개씩 총 9개
ks = ["sample_img/k1.jpg", "sample_img/k2.jpg", "sample_img/k3.jpg"]
ts = ["sample_img/t1.jpg", "sample_img/t2.jpg", "sample_img/t3.jpg"]
gs = ["sample_img/g1.jpg", "sample_img/g2.jpg", "sample_img/g3.jpg"]

food_samples = ks + ts + gs

# 이미지로 식품명 예측 후 그 식품명에 대한 영양정보 불러오기 데모
# 이미지 한개씩 모델에 적용
for i, jpg in enumerate(food_samples):
    image_file = jpg
    image = Image.open(image_file)
    
    with open(image_file, mode="rb") as image_data:
        results = classifier.classify_image(PROJECT_ID, MODEL_NAME, image_data)
    
    print("#" * 80)
    time.sleep(0.5)
    print(f"Image #{i + 1}")

    # 예측할 이미지 열기기
    plt.imshow(image)
    plt.axis("off")
    plt.show()

    time.sleep(1)
    print("Evaluating...\n")
    time.sleep(2)

    # 모델이 예측한 값들중 가장 높음 확률로 예측한 식품명과 그 확률을 변수로 저장장
    prediction = results.predictions[0]
    food_label = prediction.tag_name
    prob = prediction.probability
    print(f"음식: {food_label}\t\t Probability: {prob * 100:.2f}%\n")

    time.sleep(1)
    print("*" * 60)
    time.sleep(0.5)

    # 예측한 식품명으로 데이터베이스에서 영양정보 추출출
    print(f"Retrieving nutrition facts for {food_label} from the database...")
    time.sleep(2)
    nutrition = temp.loc[temp["식품명"] == food_label]
    display(nutrition)
    time.sleep(2)