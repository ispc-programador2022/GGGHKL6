import mysql.connector



conexion1=mysql.connector.connect(host="localhost", user="root", password="Carnaval22", auth_plugin='mysql_native_password')
cursor1=conexion1.cursor()
cursor1.execute("show database")
for base in cursor1:
    print(base)
conexion1.close