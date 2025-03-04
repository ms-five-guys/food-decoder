# 웹사이트 크롤링

## 개요
이 문서는 웹사이트에서 데이터를 크롤링하기 위한 코드와 설명을 포함합니다. Selenium과 BeautifulSoup을 사용하여 웹페이지에 접근하고 HTML을 파싱합니다.

## 라이브러리 설치
필요한 라이브러리를 설치합니다.
```bash
pip install selenium==4.17.0 typing-extensions openpyxl
pip install requests beautifulsoup4
pip install requests webdriver_manager
```

## 웹드라이버 설정 및 웹페이지 접근
Selenium을 사용하여 웹페이지에 접근하고, BeautifulSoup을 통해 HTML을 파싱합니다.

```python
from selenium import webdriver  # Selenium 웹드라이버
from selenium.webdriver.chrome.service import Service  # 웹드라이버 서비스 관리
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriver 자동 설치
from bs4 import BeautifulSoup  # HTML 파싱을 위한 BeautifulSoup
import time  # 페이지 로딩 대기 시간 설정

# 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
options.add_argument('--disable-dev-shm-usage')  # 메모리 사용 최적화

# 웹드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 대상 웹페이지 URL
url = 'https://www.allrecipes.com/'

# 웹페이지 열기
driver.get(url)

# 페이지 로딩 대기
time.sleep(3)  # 필요에 따라 조정

# 페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 웹드라이버 종료
driver.quit()
```

## 이미지 다운로드
웹페이지에서 이미지를 다운로드합니다.

```python
import requests  # 웹에서 데이터를 가져오기 위한 라이브러리
import os  # 파일 및 디렉토리 관련 작업을 위한 라이브러리

# 저장할 디렉토리 설정
save_dir = 'downloaded_images'

# 폴더가 없으면 생성
os.makedirs(save_dir, exist_ok=True)

# 이미지 태그 찾기
images = soup.find_all('img')

# 이미지 다운로드
for idx, img in enumerate(images):
    img_url = img.get('src')
    if img_url:
        try:
            # 이미지 데이터 가져오기
            img_data = requests.get(img_url).content
            # 파일 경로 설정
            img_filename = os.path.join(save_dir, f'image_{idx + 1}.jpg')
            # 이미지 저장
            with open(img_filename, 'wb') as f:
                f.write(img_data)
            print(f'Successfully downloaded {img_filename}')
        except Exception as e:
            print(f'Failed to download image at {img_url}: {e}')
```

## 결론
이 문서는 Selenium과 BeautifulSoup을 사용하여 웹사이트에서 데이터를 크롤링하고 이미지를 다운로드하는 방법을 설명합니다. 