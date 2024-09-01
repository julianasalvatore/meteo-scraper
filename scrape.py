import requests
from bs4 import BeautifulSoup
import json

def scrape_wsclima():
    url = 'https://www.wsclima.com.br/estacao/312'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Exemplo de como extrair dados (substitua pelos IDs corretos)
    temp = soup.find(id='temp').text.strip()
    umidade = soup.find(id='umidade').text.strip()

    return {
        'temperatura': temp,
        'umidade': umidade,
    }

def scrape_wunderground():
    url = 'https://www.wunderground.com/dashboard/pws/INOVAF28'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    temp = soup.find(id='temp').text.strip()
    umidade = soup.find(id='umidade').text.strip()

    return {
        'temperatura': temp,
        'umidade': umidade,
    }

def main():
    dados_wsclima = scrape_wsclima()
    dados_wunderground = scrape_wunderground()

    dados = {
        'wsclima': dados_wsclima,
        'wunderground': dados_wunderground
    }

    with open('public/dados.json', 'w') as f:
        json.dump(dados, f)

if __name__ == '__main__':
    main()
[build]
  command = "python scrape.py"
  publish = "public"
