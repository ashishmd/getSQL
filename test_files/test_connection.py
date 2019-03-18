import mysql.connector
from mysql.connector import errorcode
from test_files.test_csv_read import read_file


FILE_PATH = "test.csv"

def create_connection():
    try:
        cnx = mysql.connector.connect(user='root', database='freshsales_dev')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Datbase Exist")
        cnx.close()


def main():
    create_connection()
    


if __name__ == '__main__':
    main()

