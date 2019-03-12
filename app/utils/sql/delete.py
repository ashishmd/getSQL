from django.db import connection


def delete_data(query):
    from app.utils.sql import execute
    return execute.run_query(query)
