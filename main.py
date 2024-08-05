import mysql.connector

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    # 'database': "advanced-data-analysis",
}

# Conectar a MySQL sin especificar una base de datos
try:
    conexion = mysql.connector.connect(**config)
    print("Conexión exitosa!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    conexion = None
    
# Crear la base de datos
if conexion:
    cursor = conexion.cursor()
    nombre_base_datos = 'CompanyData'
    query_crear_bd = f"CREATE DATABASE {nombre_base_datos}"
    try:
        cursor.execute(query_crear_bd)
        print(f"Base de datos {nombre_base_datos} creada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")

# Crear la tabla
    try:
        # Cambiar a la base de datos recién creada
        cursor.execute(f"USE {nombre_base_datos}")
        
        # Definir la consulta para crear la tabla
        query_crear_tabla = """
        CREATE TABLE EmployeePerformance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            department VARCHAR(255),
            performance_score DECIMAL(5,2),
            years_with_company INT,
            salary DECIMAL(10,2)
        )
        """
        
        # Ejecutar la consulta para crear la tabla
        cursor.execute(query_crear_tabla)
        print("Tabla 'EmployeePerformance' creada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear la tabla: {err}")
    finally:
        cursor.close()
        conexion.close()
else:
    print("No se pudo conectar a la base de datos.")
