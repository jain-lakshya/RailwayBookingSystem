import mysql
import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", passwd="Lakshya@123", database="railway")
mycursor = myconn.cursor()


def close_connection():
    myconn.close()
