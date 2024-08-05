import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection(config):
    """Establece una conexión con la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Conexión exitosa!")
            return connection
    except Error as err:
        print(f"Error al conectar: {err}")
    return None

def fetch_data(connection):
    """Extrae datos de la tabla EmployeePerformance."""
    query = "SELECT * FROM EmployeePerformance"
    try:
        df = pd.read_sql(query, connection)
        print("Datos extraídos exitosamente.")
        return df
    except Error as err:
        print(f"Error al extraer datos: {err}")
    return pd.DataFrame()

def analyze_data(df):
    """Realiza el análisis de datos requerido."""
    # Asegurarse de que el DataFrame no esté vacío
    if df.empty:
        print("El DataFrame está vacío.")
        return
    
    # Calcula estadísticas para cada departamento
    stats = df.groupby('department').agg(
        performance_score_mean=('performance_score', 'mean'),
        performance_score_median=('performance_score', 'median'),
        performance_score_std=('performance_score', 'std'),
        salary_mean=('salary', 'mean'),
        salary_median=('salary', 'median'),
        salary_std=('salary', 'std'),
        employee_count=('employee_id', 'count')
    )
    
    # Calcula correlaciones
    correlation_years_performance = df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
    correlation_salary_performance = df[['salary', 'performance_score']].corr().iloc[0, 1]
    
    # Imprime resultados
    print("Estadísticas por departamento:")
    print(stats)
    
    print("\nCorrelación entre años con la empresa y puntuación de rendimiento:", correlation_years_performance)
    print("Correlación entre salario y puntuación de rendimiento:", correlation_salary_performance)

def main():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'CompanyData'
    }
    
    connection = create_connection(config)
    if connection:
        df = fetch_data(connection)
        analyze_data(df)
        connection.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    main()
