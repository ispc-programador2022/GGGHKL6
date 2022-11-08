import scraping_functions as scr
import mysql_functions as mysql
import pandas as pd
import time
import threading as th
import sys

bar = True
keep_bar = True
total = 0

country_list = []
contry_data = []
vaccine_data = []

print('Comenzando la recopilacion de datos:', end='\n\n')

def barra():
    # print('barra')
    global bar
    count = 0
    
    while bar:
        sys.stdout.write('\r')
        sys.stdout.write('.'*count)
        sys.stdout.flush()
        time.sleep(0.05)
        count = count + 1
        bar = keep_bar
    bar = True
    print() 
    
    # global bar
    # count = 0
    # while bar:
    #     print('.'*count, end='\r')
    #     time.sleep(0.5)
    #     count = count + 1
    #     bar = keep_bar
    # bar = True
    # print()  

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
        print('Lista de paises obtenida ✓')
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
        print('Datos de paises obtenidos ✓')
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
        print('Datos de paises cargados a la Base de Datos ✓')  

    get_country_thread = th.Thread(target=load)
    get_country_thread.start()
    
    barra()
    
def get_vaccine_data():
    def load():
        global keep_bar
        keep_bar = True
        
        for i in range(len(country_list)):
            v_data = scr.get_vaccine_info_by_country_url(country_list[i]['url'])
            print(v_data)
        
        keep_bar = False 
        print('Datos de vacunas obtenidos ✓') 
    
    get_country_thread = th.Thread(target=load)
    get_country_thread.start()
    
    barra()

print('Obteniendo lista de paises')
get_country_list()

# print('Obteniendo datos de paises.')
# get_contry_data()

# print('Cargado datos de paises a la Base de Datos')
# load_contry_db()

print('Obteniendo datos de vacunas por paises.')
get_vaccine_data()

