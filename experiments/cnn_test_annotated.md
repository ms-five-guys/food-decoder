# CNN 모델 테스트

## 개요
이 문서는 CNN 모델을 테스트하기 위한 코드와 설명을 포함합니다. PyTorch를 사용하여 이미지 분류 모델을 구축하고, 데이터셋을 로드하여 훈련 및 검증을 수행합니다.

## 라이브러리 설치
필요한 라이브러리를 설치합니다.
```bash
pip install torch torchvision matplotlib numpy
```

## 데이터셋 로드
데이터셋을 로드하고 전처리합니다.

```python
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

train_dataset = datasets.ImageFolder(root="sample_data/train", transform=data_transforms)
test_dataset = datasets.ImageFolder(root="sample_data/test", transform=data_transforms)
```

## DataLoader 설정
DataLoader를 설정하여 배치 단위로 데이터를 로드합니다.

```python
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
```

## CNN 모델 정의
CNN 모델을 정의합니다.

```python
import torch.nn as nn
import torch.nn.functional as F

class FoodCNN(nn.Module):
    def __init__(self, num_classes):
        super(FoodCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(in_features=128 * 16 * 16, out_features=512)
        self.fc2 = nn.Linear(in_features=512, out_features=num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

## 모델 훈련
모델을 훈련하고 검증합니다.

```python
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = FoodCNN(num_classes=5).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
```

## 모델 평가
모델을 평가하고 정확도를 출력합니다.

```python
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"테스트 정확도: {accuracy:.2f}%")
```

## 결론
이 문서는 CNN 모델을 테스트하기 위한 전체적인 과정을 설명합니다. PyTorch를 사용하여 이미지 분류 모델을 구축하고, 데이터셋을 로드하여 훈련 및 검증을 수행하는 방법을 보여줍니다. 