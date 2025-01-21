import datetime
import os
import re
import psycopg2

from dotenv import load_dotenv


class DatabaseOperations(object):

    def __init__(self):
        load_dotenv()
        self.DATABASE_URL = os.popen(os.getenv("HEROKU_COMMAND")).read()[:-1]

    def insert(self):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        loc_dt = datetime.datetime.today()
        loc_time_format = loc_dt.strftime("%H:%M:%S")
        loc_date_format = loc_dt.strftime("%Y/%m/%d")
        cursor.execute("INSERT INTO Users (Account, Password, Time, Date) VALUES (%s,%s,%s,%s)",
                       (os.getenv("USER_EXAMPLE"), os.getenv("USER_EXAMPLE_PASSWORD"), loc_time_format, loc_date_format))
        conn.commit()
        cursor.close()
        conn.close()

    def create(self):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE Users(
            ID serial PRIMARY KEY,
            Account VARCHAR (50) NOT NULL,
            Password VARCHAR (30) NOT NULL,
            Time VARCHAR (30) NOT NULL,
            Date VARCHAR (30) NOT NULL);''')
        conn.commit()
        cursor.close()
        conn.close()

    def query(self):
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        cursor.execute("SELECT Account, Password, Time, Date from Users")
        rows = cursor.fetchall()
        db0 = []
        db1 = []
        db2 = []
        db3 = []
        db4 = []
        for row in rows:
            db0.append(row[0])
            db1.append(row[1])
            db2.append(row[2])
            db3.append(row[3])
        for i in range(len(db1)):
            db4.append(
                f"{str(db0[i])}   {str(db1[i])}   {str(db2[i])}   {str(db3[i])}")
        db4 = str(db4)
        db4 = re.sub("\[|\'|\]", "", db4)
        print(db4.replace(', ', "\n"))
        cursor.close()
        conn.close()


if __name__ == "__main__":
    db = DatabaseOperations()
    db.create()
    db.insert()
