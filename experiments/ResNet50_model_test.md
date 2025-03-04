# ResNet50 모델 테스트

## 개요
이 문서는 ResNet50 모델을 사용하여 이미지 분류를 수행하는 방법을 설명합니다. PyTorch를 사용하여 모델을 로드하고, 데이터셋을 준비하여 훈련 및 평가를 진행합니다.

## 라이브러리 설치
필요한 라이브러리를 설치합니다.
```bash
pip install torch torchvision matplotlib numpy
```

## 데이터셋 준비
데이터셋을 로드하고 전처리합니다.

```python
import torchvision.transforms as transforms
from torchvision import datasets
from torch.utils.data import DataLoader

# 데이터 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 데이터셋 로드
train_dataset = datasets.ImageFolder(root='sample_data/train', transform=transform)
test_dataset = datasets.ImageFolder(root='sample_data/test', transform=transform)

# DataLoader 설정
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
```

## ResNet50 모델 로드
사전 훈련된 ResNet50 모델을 로드합니다.

```python
import torch
import torchvision.models as models

# 사전 훈련된 ResNet50 모델 로드
model = models.resnet50(pretrained=True)
model.eval()  # 평가 모드로 설정
```

## 모델 평가
모델을 평가하고 정확도를 출력합니다.

```python
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f'테스트 정확도: {accuracy:.2f}%')
```

## 결론
이 문서는 ResNet50 모델을 사용하여 이미지 분류를 수행하는 전체적인 과정을 설명합니다. PyTorch를 사용하여 모델을 로드하고, 데이터셋을 준비하여 훈련 및 평가를 진행하는 방법을 보여줍니다. 