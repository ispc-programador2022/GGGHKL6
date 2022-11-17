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
    
# --> Menu principal (✓) 
def main_menu():    
    print('')
    print('MENU PRINCIPAL:\n', '1 - Ver Base de Datos', '2 - Analisis de Base de Datos\n', '3 - SALIR', sep='\n', end='\n')
    
    ok = True
    
    try:
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
    except ValueError:
            print('Por favor, seleccione una opcion segun el numero correspondiente.')        
# <--

# --> Menu Base de Datos (✓)    
def data_base():
    print('\nBASE DE DATOS:\n')
    print('1 - Ver datos de paises', '2 - Ver tabla de vacunaciones por pais.', '3 - Editar Base de Datos', '4 - VOLVER', sep='\n', end='\n')
    
    ok = True
    
    while ok:
        try:
            choise = int(input(': '))
            
            if choise == 4:
                ok = False
                continue
            
            if choise > 3 or choise < 1:
                print('Ingrese una opción valida.')
            else:
                ok = False
                
                if choise == 1:
                    country_data()
                elif choise == 2:
                    vaccine_data()
                elif choise == 3:
                    db_edit()
        except ValueError:
            print('Por favor, seleccione una opcion segun el numero correspondiente.')
        
    main_menu()
# <--

# --> Muestra la lista de paises (✓) 
def get_country_list():
    # print(mysql.get_contry_list())
    print(pd.DataFrame({
        'Nombres': mysql.get_contry_list()
    }))
# <--

# --> Muestra los datos de paises (✓) 
def country_data():
    print('\n')
    print('DATOS DE PAISES.')
    print('Escriba el nombre del pais que desea ver. Tenga en cuanta que debe escribirlo de forma correcta, si no lo recuerda o tiene dudas ingrese "Lista" (sin comillas) para obtener la lista con los nombres de los paises.')
    print('Para volver escriba "Exit"', end='\n\n')
        
    ok = True
    
    while ok:
        choise = input('\nNombre: ').lower()
        
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
                    'Ubicacion': [country[0][4]]
                }))
    
    data_base()
# <--

# --> Muestra los datos de vacunas (✓) 
def vaccine_data():
    print('\nDATOS DE VACUNACION\n')
    print('Escriba el nombre del pais que desea ver. Tenga en cuanta que debe escribirlo de forma correcta, si no lo recuerda o tiene dudas ingrese "Lista" (sin comillas) para obtener la lista con los nombres de los paises.')
    print('Para volver escriba "Exit"', end='\n')
        
    ok = True
    
    while ok:
        choise = input('\nNombre: ').lower()
        
        if choise == 'exit':
            ok = False
            continue
        
        if choise == 'Lista':
            get_country_list()
        else:
            print(pd.DataFrame(mysql.vaccine_data_by_country(choise, True)))
    
    data_base()
# <--

# --> Menu edicion de Base de Datos (✓) 
def db_edit():
    print('\nEDICION DE BASE DE DATOS:\n')
    print('1 - Cargar un dato nuevo.', '2 - Modificar un valor. (En construccion)', '3 - Eliminar un dato. (En construccion)', '4 - VOLVER', sep='\n', end='\n')
    
    ok = True
    
    while ok:
        try:
            choise = int(input(': '))
            
            if choise == 4:
                ok = False
                continue
            
            if choise > 3 or choise < 1:
                print('Ingrese una opción valida.')
            else:
                ok = False
                
                if choise == 1:
                    add_data()
                elif choise == 2:
                    vaccine_data()
        except ValueError:
            print('Por favor, seleccione una opcion segun el numero correspondiente.')
# <--

# --> Menu de adicion de datos (✓) 
def add_data():
    print('\nAGREGAR UN DATO:\n')
    print('1 - Agregar pais.', '2 - Agregar vacunacion.', '3 - VOLVER', sep='\n', end='\n')
    
    ok = True
    
    while ok:
        try:
            choise = int(input(': '))
            
            if choise == 3:
                ok = False
                continue
            
            if choise > 2 or choise < 1:
                print('Ingrese una opción valida.')
            else:
                ok = False
                
                if choise == 1:
                    add_country()
                elif choise == 2:
                    add_vaccine()
        except ValueError:
            print('Por favor, seleccione una opcion segun el numero correspondiente.')
# <--

# --> Agrega nueva vacunacion a la DB (✓)  
def add_vaccine():
    print('\nAGREGAR VACUNACIÓN:\n')
    print('Por favor ingrese los siguientes datos:', end='\n')
        
    dato = {}   
    
    name = ['Fecha(dd/mm/aaaa): ', 'Dosis aplicadas en esta fecha: ', 'Personas vacunadas hasta la fecha:', 'Personas completamente vacunadas hasta la fecha: ', 'Pais donde se administraron: ']         
    ok = True
    
    while ok:
        resp = input('Agregar nuevo dato?(S/N): ')
        
        if resp.lower() == 'n':
            ok =False
            continue
        
        for i in range(len(name)):
            try:
                ok2 = True
                
                while ok2:                    
                    if i > 0 and i < 4:
                        valor = int(input(name[i]))
                        
                        if i == 1:
                            dato['dosis_diaria'] = valor
                        elif i == 2:
                            dato['pers_vac'] = valor
                        else:
                            dato['comp_vac'] = valor                            
                    
                    elif i == 0 or i == 4:
                        valor = input(name[i])
                        
                        if i == 0:
                            pre_fecha = valor.split('/')
                            fecha = pre_fecha[2] + '/' + pre_fecha[1] + '/' +pre_fecha[0]
                            dato['fecha'] = fecha
                        else:
                            dato['cont_name'] = valor
                    
                    ok2 = False  
                    
            except ValueError:
                i = i - 1

        dato['dosis_adm'] = mysql.get_last_vaccination(dato['cont_name'])[0][3] + dato['dosis_diaria']
        dato['por_comp_vac'] = round(dato['comp_vac'] / mysql.get_country('Argentina')[0][2] * 100, 2)
        
        print('Se almacenaran los siguientes datos:')        
        print(dato)
        resp = input('Son correctos?(S/N)')
        
        if resp.lower() == 's':
            mysql.add_vaccine_data(dato, False)
        else: 
            print('Envio cancelado.')
        
    add_data()
# <--

# --> Agregar pais a la DB (✓) 
def add_country():
    print('\nAGREGAR PAIS:\n')
    print('Por favor ingrese los siguientes datos:', end='\n')
        
    country = {}   
    
    name = ['Nombre: ', 'Población: ', 'Superficie(Km2): ', 'Continente: ']         
    ok = True
    
    while ok:
        resp = input('Agregar nuevo dato?(S/N): ')
        
        if resp.lower() == 'n':
            ok =False
            continue
        
        for i in range(len(name)):
            try:
                ok2 = True
                
                while ok2:                    
                    if i > 0 and i < 3:
                        valor = int(input(name[i]))
                        
                        if i == 1:
                            country['poblacion'] = valor
                        else:
                            country['superficie'] = valor
                            
                    elif i == 0 or i == 3:
                        valor = input(name[i])
                        
                        if i == 0:
                            country['nombre'] = valor
                        else:
                            country['continente'] = valor
                            
                    
                    ok2 = False  
                    
            except ValueError:
                i = i - 1
                
        print('Se almacenaran los siguientes datos:')        
        print(country)
        resp = input('Son correctos?(S/N)')
        
        if resp.lower() == 's':
            mysql.add_country(country)
        else: 
            print('Envio cancelado.')
# <--   

# --> Promedio de vacunaciones diarias (✓)     
def average():
    print('\nPROMEDIO DIARIO:\n')
    print('Escriba el nombre del pais para obtener el promedio de personas vacunadas por dia o el nombre del continente o "Global" para obtener el promedio por region')
    
    ok = True
    
    while ok:
        choise = input('\nNombre: ').lower()
        
        if choise == 'exit':
            ok = False
            continue
        
        if choise == 'Lista':
            get_country_list()
        else:
            data = mysql.average('dosis_diaria', choise)
            
            if data == -1:
                print('Pais no encontrado')
            else:
                print(data, 'vacunados por dia.')
    
    data_analysis()
# <--

# --> Comparación de vacunas (✓) 
def comparison():
    print('\nCOMPARACIÓN DE VACUNAS, PERSONAS, Y PERSONAS CON TODAS LAS DOSIS:\n')
    print('Escriba el nombre del pais para obtener los datos de las vacunas administradas, personas vacunadas y con todas las dosis')
    print('Escriba Lista para acceder a la lista disponible o exit para salir del menu')
    
    ok = True
    
    while ok:
        choise = input('\nNombre del pais: ').lower()
        
        if choise == 'exit':
            ok = False
            continue
        
        if choise == 'Lista':
            get_country_list()
        else:
            data = mysql.comparison(choise)
            
            if data == -1:
                print('Pais no encontrado')
            else:
                print(data)
    
    data_analysis()
# <--

# --> Menu analisis de datos (✓)  
def data_analysis():
    print('\nANALISIS DE DATOS:\n')
    print('1 - Vacunas promedio por dia', '2 - Proyeccion de vacunacion (En construccion)', '3 - Comparación de vacunación', '4 - VOLVER', sep='\n', end='\n')
    
    ok = True
    
    try:
        while ok:
            choise = int(input(': '))
            
            if choise == 4: # Ultima opcion, siempre VOLVER
                ok = False
                continue
            
            if choise > 3 or choise < 1:
                print('Ingrese una opción valida.')
            else:
                ok = False
                
                if choise == 1:
                    average() 
                elif choise == 2:
                    vaccine_data() #########
                elif choise == 3:
                    comparison()
  
    except ValueError:
            print('Por favor, seleccione una opcion segun el numero correspondiente.')
    
    main_menu()
# <--


##########

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
