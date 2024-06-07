import pymysql

# 환경 변수에서 비밀번호 로드
import os
from dotenv import load_dotenv
load_dotenv()

mysql_password = os.getenv('MYSQL_PASSWORD')

try:
    connection = pymysql.connect(
        host='49.247.34.221',
        user='root',
        password=mysql_password,
        database='woodeco'
    )
    print("Connection to the database was successful!")
    connection.close()
except pymysql.MySQLError as e:
    print(f"An error occurred: {e}")
