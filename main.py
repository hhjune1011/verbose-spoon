from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver 경로 (Raw 문자열 사용)
driver_path = 'chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저를 띄우지 않고 실행할 경우 주석 해제
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Selenium WebDriver 생성
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# Google 이미지 검색 페이지 열기
driver.get("https://www.google.com/imghp?hl=ko")

# 검색어 입력
search_box = driver.find_element(By.NAME, "q")
search_query = "사층리사진"  # 여기에 검색하고 싶은 키워드 입력
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# 이미지 탭 클릭 (명시적 대기 사용)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "이미지"))
    )
    element.click()
except Exception as e:
    print(f"이미지 탭을 찾을 수 없습니다: {e}")

# 이미지 링크 수집
time.sleep(2)  # 페이지 로드를 기다리기 위해 잠시 대기
img_links = []
for i in range(5):  # 처음부터 5페이지까지 이미지 링크 수집
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for img in soup.find_all("img", class_="rg_i Q4LuWd"):
        try:
            img_links.append(img['src'])
        except KeyError:
            continue
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    try:
        driver.find_element(By.ID, "smb").click()
        time.sleep(2)
    except:
        break

# 이미지 다운로드
save_folder = "C://Users//SAMSUNG//Desktop//python//downloaded_images"
os.makedirs(save_folder, exist_ok=True)

for idx, link in enumerate(img_links):
    img_name = f"image_{idx+1}.jpg"
    save_path = os.path.join(save_folder, img_name)
    try:
        urllib.request.urlretrieve(link, save_path)
        print(f"{img_name} 다운로드 완료")
    except Exception as e:
        print(f"{img_name} 다운로드 실패: {e}")

# WebDriver 종료
driver.quit()
