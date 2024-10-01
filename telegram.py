import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import telebot
from datetime import datetime
import pytz

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

# URL do site
url = 'https://www.wunderground.com/weather/br/nova-friburgo/INOVAF28'

def obter_dados_climaticos():
    # Fazer uma requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Inicializa o tradutor
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
        # Traduz o estado do tempo para o português
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

    # Hora Atual
    timestamp_div = soup.find('div', class_='small-12')
    if timestamp_div:
        timestamp_p = timestamp_div.find('p', class_='timestamp')
        if timestamp_p:
            timestamp_text = timestamp_p.text.strip()
            # Extrai a hora atual
            hora_atual = timestamp_text.split('GMT')[0].split(' em ')[0].strip()
            dados_climaticos['Hora Atual'] = hora_atual
        else:
            dados_climaticos['Hora Atual'] = obter_hora_atual()
    else:
        dados_climaticos['Hora Atual'] = obter_hora_atual()

    return dados_climaticos

def enviar_mensagem_telegram(chat_id, mensagem):
    bot.send_message(chat_id, mensagem, parse_mode='HTML')

@bot.message_handler(commands=['start', 'informacoes'])
def handle_start(message):
    global chat_id
    chat_id = message.chat.id
    # Adiciona um botão para solicitar informações
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = telebot.types.KeyboardButton("Obter Informações Climáticas")
    markup.add(item)
    bot.send_message(chat_id, "Bem-vindo! Pressione o botão abaixo para obter dados climáticos.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Obter Informações Climáticas")
def handle_informacoes(message):
    dados_climaticos = obter_dados_climaticos()
    mensagem = "<b>Dados Climáticos da Estação Meteorológica - Cônego</b>\n\n"
    for chave, valor in dados_climaticos.items():
        mensagem += f"{chave}: {valor}\n"
    mensagem += "\nFonte: wunderground"
    enviar_mensagem_telegram(message.chat.id, mensagem)

# Exibindo informações no terminal
dados_climaticos = obter_dados_climaticos()
print("Dados Climáticos da Estação Meteorológica - Cônego")
for chave, valor in dados_climaticos.items():
    print(f"{chave}: {valor}")
print("\nFonte: wunderground")

bot.polling()
