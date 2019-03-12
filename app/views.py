from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
from mysql.connector import errorcode
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


@login_required(login_url='/login/')
def welcome(request):
    return render(request, "welcome.html")


# Below method will check if mysql connection is working fine or not.
# It will check for db, and if found, will return success message.
@login_required(login_url='/login/')
def connection(request):
    try:
        cnx = mysql.connector.connect(user='root', database='get_sql')
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
@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def migrate_tables(request):
    from app.utils.import_export import importer
    return HttpResponse(importer.import_tables())


# below method will be used to delete all tables in the current DB.
# run migrate task after doing below operation
def reinit_db(request):
    from app.utils.sql import reinit_db
    if reinit_db.delete_all_tables():
        return HttpResponse("Success. Deleted all tables")
    else:
        return HttpResponse("Failed. Couldn't delete tables.")

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
