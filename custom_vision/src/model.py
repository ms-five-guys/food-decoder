# 커스텀 비전 클라이언트 연동 및 모델 호출
from src.config import *


# 커스텀 비전 모텔 호출
class custom_vision_model():

    def __init__(self):
        # Azure API key값과 endpoint값등 지정
        configs = get_config()
        self.ENDPOINT = configs["ENDPOINT"]
        self.KEY = configs["KEY"]
        self.PROJECT_ID = configs["PROJECT_ID"]
        self.MODEL_NAME = configs["MODEL_NAME"]
        # 위 값들로 클라이언트 인증및 연동
        self.client = get_client(ENDPOINT=self.ENDPOINT, KEY=self.KEY)

    def predict(self, image_path):
        with open(image_path, mode = "rb") as image_data:
            results = self.client.classify_image(self.PROJECT_ID, self.MODEL_NAME, image_data)

        # 모델이 예측한 값들중 가장 높음 확률로 예측한 식품명과 그 확률을 변수로 저장
        prediction = results.predictions[0]
        tag_name = prediction.tag_name
        probability = f"{prediction.probability * 100:.2f}"

        return tag_name, probability