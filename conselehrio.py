import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Função para conversão de Fahrenheit para Celsius
def fahrenheit_para_celsius(f):
    return (f - 32) * 5 / 9

# URL do site
url = 'https://www.wunderground.com/weather/br/nova-friburgo/INOVAF27'

# Fazer uma requisição HTTP para obter o conteúdo da página
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Inicializa o tradutor
translator = GoogleTranslator(source='en', target='pt')

# Função para extrair e traduzir informações
def extrair_informacoes(soup):
    dados_climaticos = {}

    # Temperatura Atual
    temp_div = soup.find('lib-display-unit', {'type': 'temperature'})
    if temp_div:
        temp_f = float(temp_div.find('span', class_='wu-value-to').text.strip())
        temp_c = fahrenheit_para_celsius(temp_f)
        dados_climaticos['Temperatura Atual'] = f"{temp_c:.1f}°C"

    # Estado do Tempo
    condition_div = soup.find('div', class_='condition-icon')
    if condition_div:
        estado_tempo = condition_div.find('p').text.strip()
        # Traduz o estado do tempo para o português
        estado_tempo_pt = translator.translate(estado_tempo)
        dados_climaticos['Estado do Tempo'] = estado_tempo_pt

    # Vento
    wind_div = soup.find('div', class_='condition-wind')
    if wind_div:
        wind_speed = wind_div.find('header', class_='wind-speed').text.strip()
        gusts_div = wind_div.find('p')
        if gusts_div:
            wind_gusts = gusts_div.find('lib-display-unit').find('span', class_='wu-value-to').text.strip()
            dados_climaticos['Vento'] = f"{wind_speed} km/h"
            dados_climaticos['Rajadas'] = f"{wind_gusts} km/h"

    return dados_climaticos

# Extrair e exibir informações
dados_climaticos = extrair_informacoes(soup)

# Exibindo os dados no terminal
print("Dados Climáticos da Estação Meteorológica - Campo do Coelho")
print()  # Espaço entre o título e os dados climáticos
for chave, valor in dados_climaticos.items():
    print(f"{chave}: {valor}")

# Espaço adicional para texto
print()  # Linha em branco para o espaço adicional
print("Fonte: wunderground")
