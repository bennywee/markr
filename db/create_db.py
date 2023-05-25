import sqlite3

def create_table():
    con = sqlite3.connect("db/markr.db")
    cur = con.cursor()

    with open("db/ddl.sql", 'r') as sql_file:
        ddl = sql_file.read()
    
    cur.execute(ddl)

if __name__ == "__main__":
    create_table()