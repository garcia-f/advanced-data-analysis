import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection(config):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Conexión exitosa!")
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None

def insert_data_from_csv(connection, csv_file):
    try:
        cursor = connection.cursor()
        df = pd.read_csv(csv_file)
        
        # Crear una lista de tuplas con los datos del DataFrame
        data = [tuple(row) for row in df.to_numpy()]
        
        # Consulta para insertar datos en la tabla
        query = """
        INSERT INTO EmployeePerformance (id, employee_id, department, performance_score, years_with_company, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(query, data)
        connection.commit()
        print("Datos insertados exitosamente.")
    except Error as err:
        print(f"Error al insertar datos: {err}")
    finally:
        cursor.close()

def main():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'CompanyData'
    }

    csv_file = 'mockaroo_data.csv'
    connection = create_connection(config)
    if connection:
        insert_data_from_csv(connection, csv_file)
        connection.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    main()
