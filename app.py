import scraping_functions as scr
import mysql_functions as mysql
import pandas as pd

pd.options.display.max_rows = None

print('#'*60)
print(f'{"#":59}#')
print(f'#{" ":4}{"BIENVENIDOS AL CENTRO DE DATOS DE VACUNAS COVID19":54}#')
print(f'{"#":59}#')
print('#'*60, end='\n\n')
print('Aqui podra obtener datos sobre las vacunas administrdas, como asi tambien filtrar por pais o continente y comparar los datos.', end='\n\n')
    
    
def main_menu():    
    print('')
    print('MENU PRINCIPAL:\n', '1 - Ver Base de Datos', '2 - Analisis de Base de Datos\n', '3 - SALIR', sep='\n', end='\n')
    
    ok = True
    
    while ok:
        choise = int(input('\n: '))
        
        if choise > 3 or choise < 1:
            print('Ingrese una opción valida.')
        else:
            ok = False
            
            if choise == 1:
                data_base()
            elif choise == 2:
                data_analysis()
            elif choise == 3:
                quit()
            
    
def data_base():
    print('\nBASE DE DATOS:\n')
    print('1 - Ver datos de paises', '2 - Ver tabla de vacunaciones por pais.', '3 - VOLVER', sep='\n', end='\n')
    
    ok = True
    
    while ok:
        choise = int(input(': '))
        
        if choise == 3:
            ok = False
            continue
        
        if choise > 2 or choise < 1:
            print('Ingrese una opción valida.')
        else:
            ok = False
            
            if choise == 1:
                country_data()
            elif choise == 2:
                vaccine_data()
    
    main_menu()

def get_country_list():
    # print(mysql.get_contry_list())
    print(pd.DataFrame({
        'Nombres': mysql.get_contry_list()
    }))
    
def country_data():
    print('\n')
    print('DATOS DE PAISES.')
    print('Escriba el nombre del pais que desea ver. Tenga en cuanta que debe escribirlo de forma correcta, si no lo recuerda o tiene dudas ingrese "Lista" (sin comillas) para obtener la lista con los nombres de los paises.')
    print('Para volver escriba "Exit"', end='\n\n')
        
    ok = True
    
    while ok:
        choise = input('\nNombre: ')
        
        if choise.lower() == 'exit':
            ok = False
            continue
        
        if choise.lower() == 'lista':
            get_country_list()
        else:
            country = mysql.get_country(choise)
            
            if len(country) == 0:
                print('No se encontro ningun pais con ese nombre. Verifique que este bien escrito.\nSi necesita ayuda escriba "Lista" para ver una lista de los paises.\n')
            else:
                print(pd.DataFrame({
                    'Pobalción': [f'{country[0][2]:,.0f} Hab.'],
                    'Superficie': [f'{country[0][3]:,.0f} Km2'],
                    'Ubicacion': ['Se ecuentra en' + country[0][4]]
                }))
    
    data_base()

def vaccine_data():
    print('\nDATOS DE VACUNACION\n')
    print('Escriba el nombre del pais que desea ver. Tenga en cuanta que debe escribirlo de forma correcta, si no lo recuerda o tiene dudas ingrese "Lista" (sin comillas) para obtener la lista con los nombres de los paises.')
    print('Para volver escriba "Exit"', end='\n')
        
    ok = True
    
    while ok:
        choise = input('\nNombre: ')
        
        if choise == 'Exit':
            ok = False
            continue
        
        if choise == 'Lista':
            get_country_list()
        else:
            print(pd.DataFrame(mysql.vaccine_data_by_country(choise)))
    
    main_menu()
    
def data_analysis():
    pass


print('MENU PRINCIPAL:\n', '1 - Ver Base de Datos', '2 - Analisis de Base de Datos\n', '3 - SALIR', sep='\n', end='\n')
    
ok = True

while ok:
    choise = int(input('\n: '))
    
    if choise > 3 or choise < 1:
        print('Ingrese una opción valida.')
    else:
        ok = False
        
        if choise == 1:
            data_base()
        elif choise == 2:
            data_analysis()
        elif choise == 3:
            quit()
        
# -->  Funcion scrapin data
# print(scr.get_vaccine_info_by_country_url('argentina'))   
# <--

# --> Funcion obtener id de Pais
# print(mysql.get_country_id('Uruguay'))  
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
# print(pd.DataFrame(mysql.vaccine_data_by_country('Afganistán')))
# <--
