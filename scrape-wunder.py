from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_temperature():
    url = 'https://www.wunderground.com/dashboard/pws/INOVAF28'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontre o seletor correto para a temperatura
    temperature_div = soup.find('div', {'class': 'current-temp'})  # Ajuste isso conforme a estrutura real do site
    temperature = temperature_div.get_text(strip=True)
    
    return temperature

@app.route('/')
def index():
    temperature = get_temperature()
    return render_template('index.html', temperature=temperature)

if __name__ == '__main__':
    app.run(debug=True)
