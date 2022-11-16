import requests
import pandas as pd
from bs4 import BeautifulSoup

Paises = ['ecuador', 'peru']

url = 'https://datosmacro.expansion.com/otros/coronavirus-vacuna/'

for pais in Paises:
    result = requests.get(url + pais).text

    soup = BeautifulSoup(result, 'lxml')

    rows = soup.find('table', id='tb0').find('tbody').find_all('tr')

    fecha = []
    dosis_adm = []
    personas_vac = []
    completo_vac = []
    porc_completo = []

    for row in rows:
        fecha.append(row.find_all('td')[0].get_text())
        dosis_adm.append(row.find_all('td')[1].get_text())
        personas_vac.append(row.find_all('td')[2].get_text())
        completo_vac.append(row.find_all('td')[3].get_text())
        porc_completo.append(row.find_all('td')[4].get_text())

    contenido = []

    contenido.append(fecha)
    contenido.append(dosis_adm)
    contenido.append(personas_vac)
    contenido.append(completo_vac)
    contenido.append(porc_completo)

    heads = soup.find('table', id='tb0').find('thead').find_all('tr')

    encabezado = []

    for head in heads:
        encabezado.append(head.find_all('th')[0].get_text())
        encabezado.append(head.find_all('th')[1].get_text())
        encabezado.append(head.find_all('th')[2].get_text())
        encabezado.append(head.find_all('th')[3].get_text())
        encabezado.append(head.find_all('th')[4].get_text())

    tabla = {}

    for campo in encabezado:
        for valores in contenido:
            tabla[campo] = valores
            contenido.remove(valores)
            break

    df = pd.DataFrame(tabla)
    print(pais.upper())

    print(df)