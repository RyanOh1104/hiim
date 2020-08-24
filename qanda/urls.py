from django.urls import path
from . import views

urlpatterns = [
    path('question', views.qandaCreate, name='question'),
    path('qandamain', views.qandaMain, name='qandamain'),
    path('answer/<int:questionNumber>', views.qandaDetail, name='qandadetail'),
    path('update/<int:questionNumber>', views.qandaUpdate, name='qandaUpdate'),

]