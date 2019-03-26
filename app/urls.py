from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
    path('connection', views.connection, name='connection'),
    path('migrate_tables', views.migrate_tables, name='migrate_tables'),
    path('migrate_columns', views.migrate_columns, name='migrate_columns'),
    path('migrate_relations', views.migrate_relations, name='migrate_relations'),
    path('reinit_db', views.reinit_db, name='reinit_db')
]
