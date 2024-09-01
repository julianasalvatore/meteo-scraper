import requests
from bs4 import BeautifulSoup
import json

def scrape_wsclima():
    url = 'https://www.wsclima.com.br/estacao/312'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Supondo que as informações estejam em tags específicas
    temperatura = soup.find('span', class_='temperature').text
    umidade = soup.find('span', class_='humidity').text
    chuva = soup.find('span', class_='rain').text
    vento = soup.find('span', class_='wind').text

    data = {
        'temperatura': temperatura,
        'umidade': umidade,
        'chuva': chuva,
        'vento': vento
    }

    with open('public/dados.json', 'w') as f:
        json.dump(data, f)

def main():
    scrape_wsclima()

if __name__ == "__main__":
    main()
