import pymysql
conn = pymysql.connect(
        host= 'database-1.c2gawlby2uqr.us-east-2.rds.amazonaws.com',
        port = 3306,
        user = 'admin',
        password = 'muni2002',
        db = 'mydb'
        )
def insert_details(name,email,comment,gender):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name,email,comment,gender))
    conn.commit()

def get_details():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM Details")
    details = cur.fetchall()
    return details