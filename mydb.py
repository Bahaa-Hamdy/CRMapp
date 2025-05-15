import mysql.connector

dataBase = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    passwd = 'Su8.wia&2',

)

# prepare a cursor object
cursorObject = dataBase.cursor()

# create a database
cursorObject.execute('CREATE DATABASE codemy')

print('ALL DONE!')

##############################################33

# import pymysql

# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='password',
#     database='codemy'
# )
# print("Connection successful!")