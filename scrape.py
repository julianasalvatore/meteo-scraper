import requests
from bs4 import BeautifulSoup

def scrape_wsclima():
    url = 'https://www.wsclima.com.br/estacao/857'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrair a temperatura
    temp_div = soup.find('div', class_='css-1p6cfa3')
    if temp_div:
        temp = temp_div.text.strip().split('º')[0]
        print(f'Temperatura no WSClima: {temp}ºC')
    else:
        print('Temperatura não encontrada no WSClima')

    # Extrair a umidade
    humidity_div = soup.find('div', class_='css-zi891l')
    if humidity_div:
        humidity = humidity_div.find('div', class_='css-0').text.strip()
        print(f'Umidade no WSClima: {humidity}')
    else:
        print('Umidade não encontrada no WSClima')

    # Extrair o índice UV
    uv_div = soup.find('div', class_='css-zi891l', text='Índice UV')
    if uv_div:
        uv_index = uv_div.find_next('div', class_='css-0').text.strip()
        print(f'Índice UV no WSClima: {uv_index}')
    else:
        print('Índice UV não encontrado no WSClima')

    # Extrair a velocidade do vento
    wind_speed_div = soup.find('div', class_='css-zi891l', text='Vel. do Vento')
    if wind_speed_div:
        wind_speed = wind_speed_div.find_next('div', class_='css-0').text.strip()
        print(f'Velocidade do Vento no WSClima: {wind_speed}')
    else:
        print('Velocidade do Vento não encontrada no WSClima')

    # Extrair a chuva acumulada
    rain_div = soup.find('div', class_='css-zi891l', text='Chuva Acumulada')
    if rain_div:
        rain = rain_div.find_next('div', class_='css-0').text.strip()
        print(f'Chuva Acumulada no WSClima: {rain}')
    else:
        print('Chuva Acumulada não encontrada no WSClima')

def main():
    scrape_wsclima()

if __name__ == "__main__":
    main()
