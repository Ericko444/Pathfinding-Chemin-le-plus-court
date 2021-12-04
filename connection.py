import pyodbc

#conn = pyodbc.connect('Driver={SQL Server};'
                     # 'Server=P13B-08-ERICKO;'
                      #'Database=Maps;'
                      #'Trusted_Connection=yes;')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-FB9Q3GV;'
                      'Database=Maps;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM Maps.dbo.Path')

for row in cursor:
    print(row[2])