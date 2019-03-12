from django.db import connection


def run_query(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return True
    except Exception as e:
        return False
