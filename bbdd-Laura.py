try:
    conexion = pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               db='peliculas')

CREATE TABLE IF NOT EXISTS paises(
    id SMALLINT(5) UNSIGNED AUTO_INCREMENT NOT NULL UNIQUE,
    nombre VARCHAR(255) UNIQUE,
    poblacion BIGINT(20) UNSIGNED NOT NULL,
    superficie BIGINT(20) UNSIGNED NOT NULL,
    continente VARCHAR(20) NOT NULL,

    PRIMARY KEY(id)
)

CREATE TABLE IF NOT EXISTS vacunas_covid19(
    id BIGINT(20) UNSIGNED AUTO_INCREMENT UNIQUE NOT NULL,
    fecha DATE,
    dosis_administradas BIGINT(20) UNSIGNED,
    personas_vacunadas  BIGINT(20) UNSIGNED,
    completamente_vacunadas BIGINT(20) UNSIGNED,
    porcentaje_completamente_vacunadas FLOAT4,
    pais_id SMALLINT(5) UNSIGNED NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(pais_id) REFERENCES paises(id)
)
