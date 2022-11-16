from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://datosmacro.expansion.com/otros/coronavirus-vacuna/paraguay"

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")
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

df = pd.DataFrame({"Fecha": fecha, "Dosis Administradas": dosis_adm, "Personas vacunadas": personas_vac,
                  "Completamente vacunadas": completo_vac, "% completamente vacunadas": porc_completo})
df
