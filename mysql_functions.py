
#CREATE TABLE IF NOT EXISTS paises(
# 	id SMALLINT(5) UNSIGNED AUTO_INCREMENT NOT NULL UNIQUE,
#     nombre VARCHAR(255) UNIQUE,
#     poblacion BIGINT(20) UNSIGNED NOT NULL,
#     superficie BIGINT(20) UNSIGNED NOT NULL,
#     continente VARCHAR(20) NOT NULL,
    
#     PRIMARY KEY(id)
# );


# CREATE TABLE IF NOT EXISTS vacunas_covid19(
# 	id BIGINT(20) UNSIGNED AUTO_INCREMENT UNIQUE NOT NULL,
#     fecha DATE,
#     dosis_administradas BIGINT(20) UNSIGNED,
#     personas_vacunadas  BIGINT(20) UNSIGNED,
#     completamente_vacunadas BIGINT(20) UNSIGNED,
#     porcentaje_completamente_vacunadas FLOAT4,
#     pais_id SMALLINT(5) UNSIGNED NOT NULL,
    
#     PRIMARY KEY(id),
#     FOREIGN KEY(pais_id) REFERENCES paises(id)
# );

import pymysql
import math

# --> Agregar un pais a la tabla paises (✓)
def add_country(country):        
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        try:
            with conection.cursor() as cursor:
                query = 'INSERT INTO paises(nombre, poblacion, superficie, continente) VALUES (%s, %s, %s, %s);'
                
                cursor.execute(query, (country['nombre'], country['poblacion'], country['superficie'], country['continente']))
                    
            conection.commit()
        finally:
            conection.close()
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Busca un pais por nombre y devuelve su id (✓)
def get_country_id(name):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        country_id = ''
        
        try:
            with conection.cursor() as cursor:
                query = 'SELECT id FROM paises WHERE nombre = "' + name + '";'
                cursor.execute(query)
                
                resp = cursor.fetchall()
                if len(resp) == 0:
                    return -1
                
                country_id = resp[0][0]
                
                return country_id

        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Agrega un nuevo dato a la tabla vacunas_covid19 (✓)        
def add_vaccine_data(dato, scraping=True):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                country_id = get_country_id(dato['cont_name'])
                
                if scraping:
                    query = 'INSERT INTO vacunas_covid19(fecha, dosis_administradas, personas_vacunadas, completamente_vacunadas, porcentaje_completamente_vacunadas, pais_id) VALUES (%s, %s, %s, %s, %s, %s);'
            
                    cursor.execute(query, (dato['fecha'], dato['dosis_adm'], dato['pers_vac'], dato['comp_vac'], dato['por_comp_vac'], country_id))
                else:
                    query = 'INSERT INTO vacunas_covid19(fecha, dosis_diaria, dosis_administradas, personas_vacunadas, completamente_vacunadas, porcentaje_completamente_vacunadas, pais_id) VALUES (%s, %s, %s, %s, %s, %s, %s);'
            
                    cursor.execute(query, (dato['fecha'], dato['dosis_diaria'], dato['dosis_adm'], dato['pers_vac'], dato['comp_vac'], dato['por_comp_vac'], country_id))
                
                conection.commit()
                
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Obtine los datos de vacunacion por nombre pais (✓)       
def vaccine_data_by_country(country, id=False):
    try:
        return_data = {
            'Fecha': [],
            'Dosis Diaria': [],
            'Dosis Administradas': [],
            'Personas Vacunadas': [],
            'Personas Completamente Vacunadas': [],
            '% Completamente Vacunado': []
        }
        
        rough_data = {}
        
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                country_id = get_country_id(country)
                
                if id:
                    return_data['id'] = []
                    query = 'SELECT fecha, dosis_diaria, dosis_administradas, personas_vacunadas, completamente_vacunadas, porcentaje_completamente_vacunadas, id FROM vacunas_covid19 WHERE pais_id = ' + str(country_id) + ' ORDER BY fecha DESC;'
                else:
                    query = 'SELECT fecha, dosis_diaria, dosis_administradas, personas_vacunadas, completamente_vacunadas, porcentaje_completamente_vacunadas FROM vacunas_covid19 WHERE pais_id = ' + str(country_id) + ' ORDER BY fecha DESC;'                
                
                cursor.execute(query)
                
                rough_data = cursor.fetchall() 
                conection.commit()
        finally:
            conection.close()
        
        for d in rough_data:
            return_data['Fecha'].append(d[0].strftime("%d/%m/%Y"))
            return_data['Dosis Diaria'].append(d[1])
            return_data['Dosis Administradas'].append(d[2])
            return_data['Personas Vacunadas'].append(d[3])
            return_data['Personas Completamente Vacunadas'].append(d[4])
            return_data['% Completamente Vacunado'].append(d[5])
            
            if id:
                return_data['id'].append(d[6]) 
        
        if not id:    
            del return_data['id']
    
        return return_data
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Obitnen los datos de un pais. (✓)
def get_country(name):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                query = 'SELECT * FROM paises WHERE nombre = "' + name + '";'
                cursor.execute(query)
                country = cursor.fetchall()
                
                return country

        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Obtine la lista completa de paises. (✓)        
def get_contry_list():
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                query = 'SELECT nombre FROM paises;'
                cursor.execute(query)
                country_list = cursor.fetchall()
                paises = []
                
                for pais in country_list:
                    paises.append(pais[0])
                
                return paises
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <-- 

# --> Actualiza un dato en la base de datos (✓)
def update_info(table, column, new_data, id):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        try:
            with conection.cursor() as cursor:
                query = 'UPDATE ' + table + ' SET ' + column + ' = %s WHERE id = %s;'
                
                cursor.execute(query, (new_data, id))
            
            conection.commit()
        
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Calcula y carga los valores de dosis diarias. (✓)    
def dosis_correction():
    lista = get_contry_list()
    print(len(lista))
    c = 1
    for pais in lista:
        c = c + 1
        data = vaccine_data_by_country(pais, id=True)
        dosis_diarias = []
        
        for i in range(len(data['Dosis Administradas'])):
            if len(data['Dosis Administradas']) == 1:
                break
            
            if i == len(data['Dosis Administradas']) - 1:    
                dosis_diarias.append(math.fsum(dosis_diarias)/len(dosis_diarias))          
                
            else:
                dosis_diarias.append(data['Dosis Administradas'][i] - data['Dosis Administradas'][i+1])
        
            update_info('vacunas_covid19', 'dosis_diaria', dosis_diarias[i], data['id'][i])
                
        print(pais + ' actualizado ✓')
# <--

# --> Devuelve el promedio de vacunaciones diarias, segun el pais o region (✓)
def average(colum, pais):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                contry_id = 0
                continentes = ['america central', 'america del sur', 'america del norte', 'asia', 'europa', 'oceania', 'africa', 'caribe']
                avg = 0
                
                if pais == 'global':
                    query = 'SELECT AVG(' + colum + ') FROM vacunas_covid19;'
                    cursor.execute(query)
                    avg = cursor.fetchall()[0][0]
                    
                elif pais.lower() in continentes:
                    query = 'SELECT AVG(' + colum +') FROM vacunas_covid19 INNER JOIN paises ON vacunas_covid19.pais_id = paises.id WHERE continente LIKE "' + pais + '";'
                    cursor.execute(query)
                    avg = cursor.fetchall()[0][0]
                else:
                    country_id = get_country_id(pais)
                    
                    if country_id == -1:
                        return -1
                    
                    query = 'SELECT AVG(' + colum +') FROM vacunas_covid19 WHERE pais_id = ' + str(country_id) + ' ;'
                    cursor.execute(query)
                    avg = cursor.fetchall()[0][0]
            
                return int(avg)
                
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Busca la ultima vacunacion por pais. (✓)
def get_last_vaccination(name):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                query = 'SELECT * FROM vacunas_covid19 WHERE pais_id = (SELECT id FROM paises WHERE nombre LIKE %s) ORDER BY fecha DESC LIMIT 1;'
                cursor.execute(query, (name))
                dosis = cursor.fetchall()
                                
                return dosis
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--        
        
