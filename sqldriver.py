import sqlite3 as sql
from venv import create

if __name__ == '__main__':
    print('no ejecutes esta wea! es una libreria uwu')
else:
    def createDB(name):
        conn = sql.connect(name)
        conn.commit()
        conn.close()
    
    def createTable(bd, name):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE '{name}' (
            name text,
            price integer
        )""")
        conn.commit()
        conn.close()

    def anyIns(bd, table, name, price):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"INSERT INTO '{table}' VALUES ('{name}', {price})"
        cursor.execute(consulta)
        conn.commit()
        conn.close()

    def itemS_all(bd, table):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"SELECT * FROM '{table}')"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos

    def itemUpdt(bd, table, name, price):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"UPDATE '{table} SET price='{price}' WHERE name='{name}')"
        cursor.execute(consulta)
        conn.commit()
        conn.close()   

# * Made by DeltaScream with Python and Coffee.