import pyodbc

with pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-ROECGEC\MSSQLSERVER01;'
                    'Database=Patient_Records_HMO_DB;'
                    'Trusted_Connection=yes;') as conn:
    cursor = conn.cursor()

