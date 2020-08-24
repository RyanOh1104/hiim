from django.urls import path
from . import views

urlpatterns = [
    path('qandacreate', views.qandaCreate, name='qandacreate'),
    path('qandamain', views.qandaMain, name='qandamain'),
    path('answer/<int:questionNumber>', views.qandaDetail, name='qandadetail'),
    path('update/<int:questionNumber>', views.qandaUpdate, name='qandaupdate'),

]