from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import mysql.connector
import json
from mysql.connector import errorcode
from app.utils.import_export import importer
from app.api import generate_sql


def index(request):
    return render(request, "index.html")


def welcome(request):
    return render(request, "welcome.html")


# Below method will check if mysql connection is working fine or not.
# It will check for db, and if found, will return success message.
def connection(request):
    try:
        cnx = mysql.connector.connect(user='root', database='get_sql', password='')
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


# Below method will import data to table app_tables
def migrate_tables(request):
    return HttpResponse(importer.import_tables())


def migrate_columns(request):
    return HttpResponse(importer.import_columns())


def migrate_relations(request):
    return HttpResponse(importer.import_relations())


def migrate_path(request):
    return HttpResponse(importer.create_path())


def migrate_all(request):
    return HttpResponse(importer.import_tables() + importer.import_columns() + importer.import_relations() +
                        importer.create_path())


def generate_query(request):
    request_data = json.loads(request.POST.get('JSONString'))
    return JsonResponse({"data": generate_sql.create_query(request_data)})


# below method will be used to delete all tables in the current DB.
# run migrate task after doing below operation
def reinit_db(request):
    from app.utils.sql import reinit_db
    if reinit_db.delete_all_tables():
        return HttpResponse("Success. Deleted all tables")
    else:
        return HttpResponse("Failed. Couldn't delete tables.")
