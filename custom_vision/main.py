################################################################################
#                           MS AI School - Five Guys                           #
################################################################################
# Korean Food Image Recognition Using Azure Custom Vision Classification Model #
################################################################################


# Imports
## 커스텀 비전 모텔 호출 자동화
from src.model import *

## 디렉토리 관리
import os


# 테스트용 이미지 불러오기
dataset_path = "custom_vision/data/test"
image_extension = ".jpg"

# 테스트용 이미지 디렉토리에서 서브디렉토리 이름들로 식품명을 불러오기
subdirs = [dir for dir in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, dir))]

# 테스트용 이미지 경로와 이름으로 레이블된 식품 이미지들을 저장할 딕셔너리 셋업
labeled_images = {label: [] for label in subdirs}

# 각 식품별 이미지 경로 저장
for label in subdirs:
    image_folder = os.path.join(dataset_path, label)

    for image in os.listdir(image_folder):
        if image.lower().endswith(image_extension):
            labeled_images[label].append(os.path.join(image_folder, image))


if __name__ == "__main__":
    custom_vision_model = custom_vision_model()
    print(f"Currently running on model: {custom_vision_model.MODEL_NAME}\n")

    # calculate the model accuracy
    total_count = 0
    accuracy_count = 0

    for label, images in labeled_images.items():
        for image in images:
            pred_label, prob = custom_vision_model.predict(image)
            
            print(f"actual: {label}\tpredicted: {pred_label}\tprobability: {prob}")
            # counter
            total_count += 1
            if label == pred_label:
                accuracy_count += 1

    print(f"Model accuracy across the entire sample dataset: {accuracy_count / total_count:.2f}")
