
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

# --> Agregar un pais a la tabla paises
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

# --> Busca un pais por nombre y devuelve su id
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
                country_id = cursor.fetchall()[0][0]
                
                return country_id

        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Agrega un nuevo dato a la tabla vacunas_covid19        
def add_vaccine_data(dato):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                country_id = get_country_id(dato['cont_name'])
                
                query = 'INSERT INTO vacunas_covid19(fecha, dosis_administradas, personas_vacunadas, completamente_vacunadas, porcentaje_completamente_vacunadas, pais_id) VALUES (%s, %s, %s, %s, %s, %s);'
            
                cursor.execute(query, (dato['fecha'], dato['dosis_adm'], dato['pers_vac'], dato['comp_vac'], dato['por_comp_vac'], country_id))
                
                conection.commit()
                
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

# --> Obtine los datos de vacunacion por nombre pais        
def vaccine_data_by_country(country):
    try:
        return_data = {
            'Fecha': [],
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
                print(country_id)
                
                query = 'SELECT fecha AS Fecha, dosis_administradas AS Dosis_Administradas, personas_vacunadas AS Personas_Vacunadas, completamente_vacunadas AS Personas_Completamente_Vacunadas, porcentaje_completamente_vacunadas AS Porc_Completamente_Vacunadas FROM vacunas_covid19 WHERE pais_id = ' + str(country_id) + ';'
                
                cursor.execute(query)
                
                rough_data = cursor.fetchall() 
                
                print(cursor.fetchall())

                conection.commit()
        finally:
            conection.close()
        
        for d in rough_data:
            return_data['Fecha'].append(d[0].strftime("%d/%m/%Y"))
            return_data['Dosis Administradas'].append(d[1])
            return_data['Personas Vacunadas'].append(d[2])
            return_data['Personas Completamente Vacunadas'].append(d[3])
            return_data['% Completamente Vacunado'].append(d[4])
            
    
        return return_data
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
# <--

def average(colum, pais):
    try:
        conection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='estadisticas_vacunas')
        
        try:
            with conection.cursor() as cursor:
                
                
                query = 'INSERT INTO vacunas_covid19(fecha, dosis_administradas, personas_vacunadas, completamente_vacunadas, porcentaje_completamente_vacunadas, pais_id) VALUES (%s, %s, %s, %s, %s, %s);'
            
                cursor.execute(query, (dato['fecha'], dato['dosis_adm'], dato['pers_vac'], dato['comp_vac'], dato['por_comp_vac'], country_id))
                
                conection.commit()
                
        finally:
            conection.close()
    
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)