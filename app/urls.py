from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('welcome', views.welcome, name='welcome'),
    path('connection', views.connection, name='connection'),
    path('migrate_tables', views.migrate_tables, name='migrate_tables'),
    path('reinit_db', views.reinit_db, name='reinit_db'),
    path('signup/', views.SignUp.as_view(), name='signup')
]
