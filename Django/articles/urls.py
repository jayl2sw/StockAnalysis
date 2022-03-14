from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.main, name='main'),
    path('corperations/', views.corperations, name='corperations'),
    path('readexcel/', views.read_excel, name='read_excel'),
    path('readdata/', views.read_data, name='read_data'),
    path('analyzeddata/', views.analyzed_data, name='analyzed_data'),
]
