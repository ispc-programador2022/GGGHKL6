import scraping_functions as scr
import mysql_functions as mysql
import pandas as pd
import time
import threading as th
import sys

bar = True
keep_bar = True
count = 0

country_list = []
contry_data = []
vaccine_data = {}

print('Comenzando la recopilacion de datos:', end='\n\n')

def clear_line():
    sys.stdout.write('\r')
    sys.stdout.write(' '*5)
    sys.stdout.write('\r')
    
def print_line(line):
    sys.stdout.write(line)
    sys.stdout.write('\n')
    sys.stdout.flush()
    sys.stdout.write('\r')
    print()

def barra():
    # print('barra')
    global bar
    global count
    count = 0
    
    while bar:
        sys.stdout.write('\r')
        sys.stdout.write('.'*count)
        sys.stdout.flush()
        time.sleep(0.075)
        count = count + 1
        if count > 5:
            clear_line()
            sys.stdout.flush()
            count = 0            
            
        bar = keep_bar
    
    clear_line()
    sys.stdout.flush()    
    bar = True
    print() 
    

def get_country_list():    
    def data():
        global country_list
        global keep_bar
        keep_bar = True
        
        country_list_urls = scr.get_countries('urls')
        country_list_names = scr.get_countries('names')
        
        for i in range(5):
            country_list.append({
                'name': country_list_names[i],
                'url': country_list_urls[i]
            })
        
        keep_bar = False        
        clear_line()
        print_line('Lista de paises obtenida ✓')
        
        print(pd.DataFrame(country_list))
        
    get_country_thread = th.Thread(target=data)
    get_country_thread.start()
    
    barra()            
        

def get_contry_data():
    def data():
        global country_list
        global contry_data
        global keep_bar
        keep_bar = True
        
        for i in range(len(country_list)):
            d = scr.get_countries_data(country_list[i]['url'])
            d['name'] = country_list[i]['name']
            
            contry_data.append(d)
            
        keep_bar = False  
        clear_line()
        print_line('Datos de paises obtenidos ✓')
        
        print(pd.DataFrame(contry_data)) 
        
    get_country_thread = th.Thread(target=data)
    get_country_thread.start()
    
    barra()
    
def load_contry_db():
    def load():
        global keep_bar
        keep_bar = True
        
        for i in range(len(contry_data)):
            mysql.add_country({
                'nombre': contry_data[i]['name'],
                'poblacion': contry_data[i]['poblacion'],
                'superficie': contry_data[i]['superficie'],
                'continente': contry_data[i]['continente']
            })
        keep_bar = False 
        clear_line()
        print_line('Datos de paises cargados a la Base de Datos ✓')
        
    get_country_thread = th.Thread(target=load)
    get_country_thread.start()
    
    barra()
    
def get_vaccine_data():
    def data():
        global keep_bar
        global vaccine_data
        keep_bar = True
        
        for i in range(len(country_list)):
            vaccine_data[country_list[i]['name']] = scr.get_vaccine_info_by_country_url(country_list[i]['url'])
            # clear_line()
            # print(vaccine_data[country_list[i]['name']])
        
        keep_bar = False 
        clear_line()
        print_line('Datos de vacunas obtenidos ✓')
    
    get_country_thread = th.Thread(target=data)
    get_country_thread.start()
    
    barra()


def load_vaccine_data_db():
    def load():
        global keep_bar
        global vaccine_data
        keep_bar = True
        
        dato = {}
        
        for pais in vaccine_data:
            for i in range(len(vaccine_data[pais].axes[0])):
                pre_fecha = vaccine_data[pais].loc[i, vaccine_data[pais].columns.values[0]].split('/')
                fecha = pre_fecha[2] + '/' + pre_fecha[1] + '/' +pre_fecha[0]
                
                dato['fecha'] = fecha
                dato['dosis_adm'] = int(vaccine_data[pais].loc[i, vaccine_data[pais].columns.values[1]])
                dato['pers_vac'] = int(vaccine_data[pais].loc[i, vaccine_data[pais].columns.values[2]])
                dato['comp_vac'] = int(vaccine_data[pais].loc[i, vaccine_data[pais].columns.values[3]])
                dato['por_comp_vac'] = float(vaccine_data[pais].loc[i, vaccine_data[pais].columns.values[4]])
                dato['cont_name'] = pais
                
                mysql.add_vaccine_data(dato)            

            print(dato)
        
        keep_bar = False 
        clear_line()
        print_line('Datos de vacunas cargado a la Base de Datos ✓')
        
    get_country_thread = th.Thread(target=load)
    get_country_thread.start()
    
    barra()

print('Obteniendo lista de paises')
get_country_list()
time.sleep(0.5)

print('Obteniendo datos de paises.')
get_contry_data()
time.sleep(0.5)

print('Cargado datos de paises a la Base de Datos')
load_contry_db()
time.sleep(0.5)

print('Obteniendo datos de vacunas.')
get_vaccine_data()
time.sleep(0.5)

print('Cargando datos de vacunas a la Base de Datos.')
load_vaccine_data_db()
time.sleep(0.5)

# print(int(vaccine_data['Afganistán'].loc[0, vaccine_data['Afganistán'].columns.values[1]]))
# , data_frame.columns.values[col]