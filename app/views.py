from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
from mysql.connector import errorcode


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def welcome(request):
    return render(request, "welcome.html")


def connection(request):
    try:
        cnx = mysql.connector.connect(user='root', database='freshsales_dev')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return HttpResponse("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return HttpResponse("Database does not exist")
        else:
            return HttpResponse(err)
    else:
        cnx.close()
        return HttpResponse("Connection Success. Database Exist")


def migrate_tables(request):
    from app.utils.import_export import importer
    return HttpResponse(importer.import_tables())


def reinit_db(request):
    from app.utils.sql import reinit_db
    if reinit_db.delete_all_tables():
        return HttpResponse("Success. Deleted all tables")
    else:
        return HttpResponse("Failed. Couldn't delete tables.")
