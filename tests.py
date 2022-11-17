import mysql_functions as mysql
import scraping_functions as scr
import pandas as pd
import math
# print(mysql.get_country('Argentina'))
pd.options.display.max_rows = None

# print(mysql.dosis_correction())
# print(pd.DataFrame(mysql.get_contry_list()))
# print(mysql.average('dosis_diaria', 'Argentina'))
print(round(40000000 / mysql.get_country('Argentina')[0][2] * 100, 2))