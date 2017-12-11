import pyodbc

db_path = "university_A1.mdb"
database = pyodbc.connect("DRIVER={Microsoft Access Driver (*.mdb)};DBQ=" + db_path)

if __name__ == '__main__':
	cursor = database.cursor()
