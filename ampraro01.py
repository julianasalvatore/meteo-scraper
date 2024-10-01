import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime, timedelta
import pytz
import re

# Função para conversão de Fahrenheit para Celsius
def fahrenheit_para_celsius(f):
    return (f - 32) * 5 / 9

# Função para ajustar a hora para o horário de Brasília
def ajustar_hora_brasilia(hora_gmt_str, segundos_atualizacao):
    # Parse da string de hora GMT
    hora_gmt = datetime.strptime(hora_gmt_str, '%I:%M %p')
    gmt_timezone = pytz.timezone('GMT')
    brasilia_timezone = pytz.timezone('America/Sao_Paulo')
    
    # Adiciona a data do sistema para a hora
    hora_gmt = gmt_timezone.localize(hora_gmt)
    hora_brasilia = hora_gmt.astimezone(brasilia_timezone)
    
    # Subtrai os segundos da atualização
    hora_brasilia_atualizada = hora_brasilia - timedelta(seconds=segundos_atualizacao)
    
    return hora_brasilia_atualizada

# URL do site
url = 'https://www.wunderground.com/weather/INOVAF23'

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

    # Hora Atual e Atualização
    timestamp_div = soup.find('p', class_='timestamp')
    if timestamp_div:
        # Extrair a hora e o tempo de atualização
        hora_atual_match = re.search(r'(\d{1,2}:\d{2} [APM]{2}) GMT-03:00', timestamp_div.text)
        atualizacao_match = re.search(r'Atualizado há (\d+) segundos', timestamp_div.text)

        if hora_atual_match and atualizacao_match:
            hora_atual_str = hora_atual_match.group(1)
            segundos_atualizacao = int(atualizacao_match.group(1))
            
            # Ajustar a hora para o horário de Brasília
            hora_brasilia_atualizada = ajustar_hora_brasilia(hora_atual_str, segundos_atualizacao)
            dados_climaticos['Hora Atual'] = hora_brasilia_atualizada.strftime('%H:%M')
            dados_climaticos['Atualização'] = f"Atualizado há {segundos_atualizacao} segundos"

    return dados_climaticos

# Extrair e exibir informações
dados_climaticos = extrair_informacoes(soup)

# Exibindo os dados no terminal
print("Dados Climáticos da Estação Meteorológica - Amparo 01")
print()  # Espaço entre o título e os dados climáticos
for chave, valor in dados_climaticos.items():
    print(f"{chave}: {valor}")

# Espaço adicional para texto
print()  # Linha em branco para o espaço adicional
print("Fonte: wunderground")
