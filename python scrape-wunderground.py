import requests
from bs4 import BeautifulSoup

# Funções para conversão de unidades
def fahrenheit_para_celsius(f):
    return (f - 32) * 5 / 9

def mph_para_kmh(mph):
    return mph * 1.60934

def hpa_para_inhg(hpa):
    return hpa / 33.8639

# Função para extrair informações
def extrair_informacoes(soup):
    dados_climaticos = {}

    # Temperatura Atual
    temp_div = soup.find('div', class_='module__body').find_all('span', class_='wu-value-to')
    if temp_div:
        temp_f = float(temp_div[0].text.strip())
        dados_climaticos['Temperatura Atual'] = f"{fahrenheit_para_celsius(temp_f):.1f}°C"

    # Sensação Térmica
    feels_like_div = soup.find('div', class_='weather__header', text='Feels Like')
    if feels_like_div:
        feels_like_f = float(feels_like_div.find_next('span', class_='wu-value-to').text.strip())
        dados_climaticos['Sensação Térmica'] = f"{fahrenheit_para_celsius(feels_like_f):.1f}°C"

    # Vento e Rajadas
    wind_div = soup.find('div', class_='weather__wind-gust')
    if wind_div:
        wind_text = wind_div.find('div', class_='weather__text').text.strip()
        wind_text = wind_text.replace('\xa0', '')  # Remove espaço não separável
        vento_mph, rajadas_mph = [float(x.split('°')[0].strip()) for x in wind_text.split(' / ')]
        dados_climaticos['Vento e Rajadas'] = f"{mph_para_kmh(vento_mph):.1f} km/h / {mph_para_kmh(rajadas_mph):.1f} km/h"

    # Ponto de Orvalho
    dewpoint_div = soup.find('div', class_='weather__header', text='DEWPOINT')
    if dewpoint_div:
        dewpoint_f = float(dewpoint_div.find_next('span', class_='wu-value-to').text.strip())
        dados_climaticos['Ponto de Orvalho'] = f"{fahrenheit_para_celsius(dewpoint_f):.1f}°C"

    # Taxa de Precipitação
    precip_rate_div = soup.find('div', class_='weather__header', text='PRECIP RATE')
    if precip_rate_div:
        precip_rate_mm = float(precip_rate_div.find_next('span', class_='wu-value-to').text.strip())
        dados_climaticos['Taxa de Precipitação'] = f"{precip_rate_mm:.2f} mm/h"

    # Pressão Atmosférica
    pressure_div = soup.find('div', class_='weather__header', text='PRESSURE')
    if pressure_div:
        pressure_inhg = float(pressure_div.find_next('span', class_='wu-value-to').text.strip())
        dados_climaticos['Pressão Atmosférica'] = f"{pressure_inhg * 33.8639:.1f} hPa"

    # Umidade Relativa
    humidity_div = soup.find('div', class_='weather__header', text='HUMIDITY')
    if humidity_div:
        dados_climaticos['Umidade Relativa'] = humidity_div.find_next('span', class_='wu-value-to').text.strip() + '%'

    # Precipitação Acumulada
    precip_accum_div = soup.find('div', class_='weather__header', text='PRECIP ACCUM')
    if precip_accum_div:
        precip_accum_mm = float(precip_accum_div.find_next('span', class_='wu-value-to').text.strip())
        dados_climaticos['Precipitação Acumulada'] = f"{precip_accum_mm:.2f} mm"

    # Índice UV
    uv_div = soup.find('div', class_='weather__header', text='UV')
    if uv_div:
        dados_climaticos['Índice UV'] = uv_div.find_next('span', class_='wu-value-to').text.strip()

    return dados_climaticos

# URLs e Títulos
links = [
    ('https://www.wunderground.com/dashboard/pws/INOVAF28', "Dados Climáticos da Estação Meteorológica - Três Picos"),
 ]

# Função principal
def main():
    for url, titulo in links:
        # Fazer uma requisição HTTP para obter o conteúdo da página
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        dados_climaticos = extrair_informacoes(soup)

        # Exibindo o título e os dados no terminal
        print(titulo)
        print()  # Espaço entre o título e os dados climáticos
        print("Dados Climáticos:")
        for chave, valor in dados_climaticos.items():
            print(f"{chave}: {valor}")

        # Espaço adicional para texto
        print()  # Linha em branco para o espaço adicional
        texto_adicional = input("Fonte: ")
        print(texto_adicional)
        print()  # Linha em branco para separar as estações

if __name__ == "__main__":
    main()
