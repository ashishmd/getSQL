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
    from app.utils.import_export.importer import import_tables
    return HttpResponse(import_tables())

