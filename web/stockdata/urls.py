from django.urls import path
from . import views

app_name = 'stockdata'

urlpatterns = [
    path('', views.main, name='main') ,
    path('<str:corp_code>/', views.detail, name='detail'),
    path('<str:corp_code>/delete', views.delete, name='delete'),

]
