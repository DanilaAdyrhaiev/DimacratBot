import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_google_drive_folder(folder_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(folder_url)
        time.sleep(3)

        last_count = 0
        while True:
            elements = driver.find_elements(By.CSS_SELECTOR, ".pmHCK")
            if elements:
                driver.execute_script("arguments[0].scrollIntoView();", elements[-1])
                time.sleep(2)

            new_count = len(driver.find_elements(By.CSS_SELECTOR, ".pmHCK"))
            if new_count == last_count:
                break
            last_count = new_count

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pmHCK"))
        )

        chapters = []
        chapter_elements = driver.find_elements(By.CSS_SELECTOR, ".tyTrke .KL4NAf")
        document_elements = driver.find_elements(By.CSS_SELECTOR, "[jsdata^='KCtMme;']")

        for chapter, doc in zip(chapter_elements, document_elements):
            chapter_text = chapter.text.strip()
            chapter_number = chapter_text.split()[0] if chapter_text else ""
            jsdata_value = doc.get_attribute("jsdata")
            if jsdata_value:
                document_id = jsdata_value.split(';')[1]
                document_link = f"https://docs.google.com/document/d/{document_id}"
                chapters.append({'chapter': chapter_number, 'link': document_link})

        # Возвращаем данные в формате JSON
        return json.dumps(chapters, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

folder_url = "https://drive.google.com/drive/folders/1AlSxIUa4blLG2e3tEHPzceB3NnjIPike"
results = parse_google_drive_folder(folder_url)
print(results)

