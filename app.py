import scraping_functions as scr
import mysql_functions as mysql
import pandas as pd

print('#'*60)
print(f'{"#":59}#')
print(f'#{" ":4}{"BIENVENIDOS AL CENTRO DE DATOS DE VACUNAS COVID19":54}#')
print(f'{"#":59}#')
print('#'*60, end='\n\n')
print('Aqui podra obtener datos sobre las vacunas administrdas, como asi tambien filtrar por pais o continente y comparar los datos.')

# -->  Funcion scrapin data
# print(scr.get_vaccine_info_by_country_url('argentina'))   
# <--

# --> Funcion obtener id de Pais
# print(mysql.get_country_id('Argentina'))  
# <--

# --> Estructura de ingreso de dato
# dato = {                             
#     'fecha': '10/12/22',
#     'dosis_adm': 123123,
#     'pers_vac': 1345134,
#     'comp_vac': 12312,
#     'por_comp_vac': 34.8,
#     'cont_name': 'Brasil'
# }
# <--

# --> Funcion agregar dato
# mysql.add_vaccine_data(dato)         
# <--

# --> Estructura ingreso de dato pais
# country = {                           
#     'nombre': 'Brasil',
#     'poblacion': 12341234,
#     'superficie': 13123123,
#     'continente': 'America del Sur'
# }
# <--

# --> Funcion Agregar pais
# mysql.add_country(country)
# <--

# --> Impresion datos por pais
# print(pd.DataFrame(mysql.vaccine_data_by_country('Argentina')))
# <--
