import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrap (f):

    url= 'https://datosmacro.expansion.com/otros/coronavirus-vacuna/'

    result = requests.get(url+f).text

    soup = BeautifulSoup(result, 'lxml')

    rows = soup.find('table', id='tb0').find('tbody').find_all('tr')

    #Cantidad de columnas td

    for tr in rows:
        tds =[]
        for td in tr:
            tds.append(td.text)

    cant = len(tds)

    #Valores de columnas 

    conj_tds = []

    for x in range(cant):
        colum_x = []
        for row in rows:
            colum_x.append(row.find_all('td')[x].get_text())
            
        conj_tds.append(colum_x)

    #Parte de encabezado

    heads = soup.find('table', id='tb0').find('thead').find_all('tr')

    encabezado = []

    for tr in heads:
        for th in tr:
            encabezado.append(th.text)
            
    #Consolidado de tabla
    
    tabla={}

    for campo in  encabezado:
        for valores in conj_tds:
          tabla[campo] = valores
          conj_tds.remove(valores)
          break
        
        
    df = pd.DataFrame(tabla)

    return df

país = input('Ingrese el país: ')

print(scrap(país))