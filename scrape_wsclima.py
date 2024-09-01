from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_wsclima():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.wsclima.com.br/estacao/857")

        while True:
            try:
                # Aguarde até que o elemento da temperatura esteja presente
                temperatura_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1p6cfa3'))
                )
                
                # Extraia a temperatura e sensação
                temperatura = temperatura_element.text.split('º')[0].strip()
                
                sensacao_element = temperatura_element.find_element(By.CSS_SELECTOR, 'p.chakra-text.css-16vhagl')
                sensacao = sensacao_element.text.split(' ')[2].strip()

                print(f"Temperatura: {temperatura} ºC")
                print(f"Sensação Térmica: {sensacao} ºC")

            except Exception as e:
                print(f"Ocorreu um erro ao coletar dados: {str(e)}")

            time.sleep(180)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_wsclima()
