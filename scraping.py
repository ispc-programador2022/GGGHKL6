import requests

from bs4 import BeautifulSoup

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
url = 'https://datosmacro.expansion.com/otros/coronavirus-vacuna/'

paises = ['guyana', 'surinam']

data = {}

for pais in paises:
    url_data = url + pais
    r = requests.get(url_data, headers=headers, timeout=5).text
    s = BeautifulSoup(r, 'lxml')
        
    table_data = s.find('table', id='tb0')
    tbody = table_data.find_all('tr')

    row_data = []

    for tr in tbody:
        tr_array = []
        for td in tr:
            tr_array.append(td.text)
            
        row_data.append(tr_array)
        
    data[pais] = row_data

    
for line in data['surinam']:
    for value in line:
        print(f'{value:25}', end=' ')
    print()