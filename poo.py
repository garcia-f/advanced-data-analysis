import mysql.connector as connection
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine

class DatabaseManager:
    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host
        self.engine = None

    def create_database(self, db_name):
        try:
            mydb = connection.connect(
                host=self.host,
                user=self.user, 
                passwd=self.password
            )
            cursor = mydb.cursor()
            query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
            cursor.execute(query)
            mydb.close()
        except Exception as e:
            print(f"Error creating database: {str(e)}")

    def create_table(self, db_name):
        try:
            mydb = connection.connect(
                host=self.host,
                database=db_name,
                user=self.user, 
                passwd=self.password
            )
            cursor = mydb.cursor()
            query = '''
            CREATE TABLE IF NOT EXISTS employeeperformance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT NOT NULL,
                department VARCHAR(255) NOT NULL,
                performance_score DECIMAL(10, 2) NOT NULL,
                years_with_company INT NOT NULL,
                salary DECIMAL(10, 2) NOT NULL
            );
            '''
            cursor.execute(query)
            mydb.close()
        except Exception as e:
            print(f"Error creating table: {str(e)}")

    def connect_to_engine(self, db_name):
        try:
            connection_query = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{db_name}'
            self.engine = create_engine(connection_query)
        except Exception as e:
            print(f"Error connecting to engine: {str(e)}")

class EmployeePerformanceData:
    def __init__(self, engine):
        self.engine = engine
        self.data_frame = None

    def load_data(self):
        query = "SELECT * FROM employeeperformance;"
        self.data_frame = pd.read_sql(query, con=self.engine)

    def load_from_csv_if_empty(self, csv_path):
        if self.data_frame is None or self.data_frame.empty:
            data = pd.read_csv(csv_path)
            data.to_sql('employeeperformance', con=self.engine, if_exists='append', index=False)
            self.load_data()

class EmployeePerformanceAnalysis:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def total_employees_per_department(self):
        return self.data_frame.groupby(by="department").count()["employee_id"]

    def mean_median_std_performance_score(self):
        groupby_department = self.data_frame.groupby(by="department")
        return {
            "mean": groupby_department.mean()["performance_score"],
            "median": groupby_department.median()["performance_score"],
            "std": groupby_department.std()["performance_score"],
        }

    def mean_median_std_salary(self):
        groupby_department = self.data_frame.groupby(by="department")
        return {
            "mean": groupby_department.mean()["salary"],
            "median": groupby_department.median()["salary"],
            "std": groupby_department.std()["salary"],
        }

    def correlation_year_performance(self):
        correlation = pd.DataFrame({
            "department": self.data_frame["department"],
            "years_with_company": self.data_frame["years_with_company"],
            "performance_score": self.data_frame["performance_score"]
        })
        return correlation.groupby(by="department").corr()["years_with_company"].unstack()["performance_score"]

    def correlation_salary_performance(self):
        correlation = pd.DataFrame({
            "department": self.data_frame["department"],
            "salary": self.data_frame["salary"],
            "performance_score": self.data_frame["performance_score"]
        })
        return correlation.groupby(by="department").corr()["salary"].unstack()["performance_score"]

    def hist_performance_per_department(self):
        department_performance = self.data_frame.groupby(by="department").mean()
        plt.bar(department_performance.index, department_performance["performance_score"])
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def scatter_years_performance(self):
        plt.scatter(self.data_frame["years_with_company"], self.data_frame["performance_score"])
        plt.xlabel("Años en la compañia")
        plt.ylabel("Rendimiento")
        plt.show()

    def scatter_salary_performance(self):
        plt.scatter(self.data_frame["performance_score"], self.data_frame["salary"])
        plt.xlabel("Rendimiento")
        plt.ylabel("Salario")
        plt.show()


# Configuración de la base de datos
db_manager = DatabaseManager(user="root", password="", host="localhost")
db_manager.create_database("companydata")
db_manager.create_table("companydata")
db_manager.connect_to_engine("companydata")

# Carga de datos
data_manager = EmployeePerformanceData(engine=db_manager.engine)
data_manager.load_data()
data_manager.load_from_csv_if_empty("mockaroo_data.csv")

# Análisis de datos
analysis = EmployeePerformanceAnalysis(data_frame=data_manager.data_frame)
print(analysis.total_employees_per_department())
print(analysis.mean_median_std_performance_score())
print(analysis.mean_median_std_salary())
print(analysis.correlation_year_performance())
print(analysis.correlation_salary_performance())
analysis.hist_performance_per_department()
analysis.scatter_years_performance()
analysis.scatter_salary_performance()
          