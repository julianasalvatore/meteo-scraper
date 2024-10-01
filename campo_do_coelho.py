import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import telebot
from datetime import datetime, timedelta
import pytz
import re

# Configuração do bot do Telegram
TELEGRAM_TOKEN = '7508349020:AAEva-rrifb2cnLK0psWd9R5SbX_pssZOck'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Função para conversão de Fahrenheit para Celsius
def fahrenheit_para_celsius(f):
    return (f - 32) * 5 / 9

# Função para capturar a hora atual
def obter_hora_atual():
    timezone_br = pytz.timezone('America/Sao_Paulo')
    hora_atual = datetime.now(timezone_br).strftime('%H:%M')
    return hora_atual

# Função para ajustar a hora para o horário de Brasília
def ajustar_hora_brasilia(hora_gmt_str, segundos_atualizacao):
    hora_gmt = datetime.strptime(hora_gmt_str, '%I:%M %p')
    gmt_timezone = pytz.timezone('GMT')
    brasilia_timezone = pytz.timezone('America/Sao_Paulo')
    hora_gmt = gmt_timezone.localize(hora_gmt)
    hora_brasilia = hora_gmt.astimezone(brasilia_timezone)
    hora_brasilia_atualizada = hora_brasilia - timedelta(seconds=segundos_atualizacao)
    return hora_brasilia_atualizada

# Função para extrair dados climáticos da URL
def obter_dados_climaticos(url, station_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    translator = GoogleTranslator(source='en', target='pt')

    dados_climaticos = {}

    # Temperatura Atual
    temp_div = soup.find('lib-display-unit', {'type': 'temperature'})
    if temp_div:
        temp_f = float(temp_div.find('span', class_='wu-value-to').text.strip())
        temp_c = fahrenheit_para_celsius(temp_f)
        dados_climaticos['Temperatura Atual'] = f"{temp_c:.1f}°C"
    else:
        dados_climaticos['Temperatura Atual'] = "Não disponível"

    # Estado do Tempo
    condition_div = soup.find('div', class_='condition-icon')
    if condition_div:
        estado_tempo = condition_div.find('p').text.strip()
        estado_tempo_pt = translator.translate(estado_tempo)
        dados_climaticos['Estado do Tempo'] = estado_tempo_pt
    else:
        dados_climaticos['Estado do Tempo'] = "Não disponível"

    # Vento
    wind_div = soup.find('div', class_='condition-wind')
    if wind_div:
        wind_speed = wind_div.find('header', class_='wind-speed').text.strip()
        gusts_div = wind_div.find('p')
        if gusts_div:
            wind_gusts = gusts_div.find('lib-display-unit').find('span', class_='wu-value-to').text.strip()
            dados_climaticos['Vento'] = f"{wind_speed} km/h"
            dados_climaticos['Rajadas'] = f"{wind_gusts} km/h"
        else:
            dados_climaticos['Vento'] = "Não disponível"
            dados_climaticos['Rajadas'] = "Não disponível"
    else:
        dados_climaticos['Vento'] = "Não disponível"
        dados_climaticos['Rajadas'] = "Não disponível"

    # Hora Atual e Atualização
    timestamp_div = soup.find('p', class_='timestamp')
    if timestamp_div:
        hora_atual_match = re.search(r'(\d{1,2}:\d{2} [APM]{2}) GMT-03:00', timestamp_div.text)
        atualizacao_match = re.search(r'Atualizado há (\d+) segundos', timestamp_div.text)

        if hora_atual_match and atualizacao_match:
            hora_atual_str = hora_atual_match.group(1)
            segundos_atualizacao = int(atualizacao_match.group(1))
            hora_brasilia_atualizada = ajustar_hora_brasilia(hora_atual_str, segundos_atualizacao)
            dados_climaticos['Hora Atual'] = hora_brasilia_atualizada.strftime('%H:%M')
        else:
            dados_climaticos['Hora Atual'] = obter_hora_atual()

    return dados_climaticos

def enviar_mensagem_telegram(chat_id, mensagem):
    bot.send_message(chat_id, mensagem, parse_mode='HTML')

@bot.message_handler(commands=['start', 'informacoes'])
def handle_start(message):
    global chat_id
    chat_id = message.chat.id
    # Adiciona botões para solicitar informações de diferentes estações
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Cônego")
    item2 = telebot.types.KeyboardButton("Caledonia")
    markup.add(item1, item2)
    bot.send_message(chat_id, "Bem-vindo! Pressione um dos botões abaixo para obter dados climáticos.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Cônego")
def handle_informacoes_conego(message):
    url = 'https://www.wunderground.com/weather/br/nova-friburgo/INOVAF28'
    dados_climaticos = obter_dados_climaticos(url, 'Cônego')
    mensagem = "<b>Dados Climáticos da Estação Meteorológica - Cônego</b>\n\n"
    for chave, valor in dados_climaticos.items():
        mensagem += f"{chave}: {valor}\n"
    mensagem += "\nFonte: wunderground"
    enviar_mensagem_telegram(message.chat.id, mensagem)

@bot.message_handler(func=lambda message: message.text == "Caledonia")
def handle_informacoes_caledonia(message):
    url = 'https://www.wunderground.com/weather/br/nova-friburgo/INOVAF18'
    dados_climaticos = obter_dados_climaticos(url, 'Caledonia')
    mensagem = "<b>Dados Climáticos da Estação Meteorológica - Caledonia</b>\n\n"
    for chave, valor in dados_climaticos.items():
        mensagem += f"{chave}: {valor}\n"
    mensagem += "\nFonte: wunderground"
    enviar_mensagem_telegram(message.chat.id, mensagem)

# Exibindo informações no terminal
url_conego = 'https://www.wunderground.com/weather/br/nova-friburgo/INOVAF28'
dados_climaticos_conego = obter_dados_climaticos(url_conego, 'Cônego')
print("Dados Climáticos da Estação Meteorológica - Cônego")
for chave, valor in dados_climaticos_conego.items():
    print(f"{chave}: {valor}")
print("\nFonte: wunderground")

url_caledonia = 'https://www.wunderground.com/weather/br/nova-friburgo/INOVAF18'
dados_climaticos_caledonia = obter_dados_climaticos(url_caledonia, 'Caledonia')
print("\nDados Climáticos da Estação Meteorológica - Caledonia")
for chave, valor in dados_climaticos_caledonia.items():
    print(f"{chave}: {valor}")
print("\nFonte: wunderground")

bot.polling()
