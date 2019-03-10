from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def welcome(request):
    return render(request, "welcome.html")


def connection(request):
    from django.db import connections
    from django.db.utils import OperationalError
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        return HttpResponse("Connection failed")
    else:
        return HttpResponse("Connection success")

