import mysql_functions as mysql
import scraping_functions as scr
import pandas as pd
# print(mysql.get_country('Argentina'))
pd.options.display.max_rows = None

paises = mysql.get_contry_list()
print(paises)