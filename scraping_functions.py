import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
baseURL = 'https://datosmacro.expansion.com'

def get_countries(prop):
    url = baseURL + '/paises'  
    
    r = requests.get(url, headers=headers, timeout=5).text
    s = BeautifulSoup(r, 'lxml')

    countries_element = s.find('div', class_='flags') 
    
    if prop == 'urls':
        countries_urls = []
        
        for div in countries_element:
            country_url = div.find('a').attrs['href'][8:]
            countries_urls.append(country_url)
        return countries_urls
    
    elif prop == 'names':
        countries_names = []
        
        for div in countries_element:
            country_name = div.h4.a.text
            countries_names.append(country_name)
        
        return countries_names
    

def get_countries_data(country_url):
    url = baseURL + '/paises/' + country_url
    
    r = requests.get(url, headers=headers, timeout=5).text
    s = BeautifulSoup(r, 'lxml')
    
    cuadros = s.find_all('div', class_='cuadro')
    info = s.find('div', itemprop='articleBody')
    
    continent = info.p.text.split(',')[1][11:]
    
    population = ''
    surface = ''
    
    for li in cuadros[1].ul:        
        if li.span.text == 'Población':
            population = int(''.join(li.text.split(": ")[1].split('.')))
            
        if li.span.text == 'Superficie':
            surface = int(''.join(li.text.split(" ")[1].split('.')))
    
    h1 = s.find('h1').find_all('a')[1].text.split(':')[0]
    
    # print(f'Datos obtenidos de: {h1} ✓')
    sys.stdout.write('\r')
    sys.stdout.write('')
    sys.stdout.flush()
    print(f'Datos obtenidos de: {h1} ✓')
    
    return {
        'poblacion': population,
        'superficie': surface,
        'continente': continent
    }
    

def get_vaccine_info_by_country_url(country_url):
    url = baseURL + '/otros/coronavirus-vacuna/' + country_url
    
    r = requests.get(url, headers=headers, timeout=5).text
    s = BeautifulSoup(r, 'lxml')
    
    table_data = s.find('table', id='tb0')
    header = table_data.thead.find_all('th')
    
    data = {}
    
    for th in header:
        data[th.text] = []
    
    data_frame = pd.DataFrame(data)
    print(data_frame)
    
    values_row = table_data.tbody.find_all('tr')

    print(data_frame.columns.values)
    
    index = 0
    for tr in values_row:
        col = 0
        for td in tr:
            data_frame.loc[index, data_frame.columns.values[col]] = td.text
            col = col + 1
        
        index = index + 1        
    
    table_name = s.find('h1').find_all('a')[1].text
    
    print(f'Tabla obtenida: {table_name}')
    
    return data_frame
    
    