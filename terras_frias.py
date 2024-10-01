from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configurações do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless, sem abrir a janela

# Caminho para o ChromeDriver
service = Service('CAMINHO_PARA_O_SEU_CHROMEDRIVER')

# Iniciando o navegador
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessar a URL da página
driver.get("URL_DA_PAGINA")

# Aguardar alguns segundos para garantir que a página carregue o conteúdo dinâmico
time.sleep(5)

# Extrair a temperatura
try:
    temperatura_element = driver.find_element(By.CLASS_NAME, "css-1p6cfa3")
    temperatura = temperatura_element.text
    print(f"Temperatura: {temperatura}")
except:
    print("Temperatura não encontrada!")

# Extrair a sensação térmica
try:
    sensacao_termica_element = driver.find_element(By.CLASS_NAME, "css-16vhagl")
    sensacao_termica = sensacao_termica_element.text
    print(f"Sensação térmica: {sensacao_termica}")
except:
    print("Sensação térmica não encontrada!")

# Fechar o navegador
driver.quit()
