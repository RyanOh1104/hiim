from django.urls import path
from . import views

urlpatterns = [
    path('question', views.qandaInput, name='qandaInput'),
    path('qandamain', views.qandaMain, name='qandaMain'),
    path('no-more-for-today', views.noMoreForToday, name='noMoreForToday'),
    path('answer/<int:questionNumber>', views.qandaDetail, name='qandadetail'),
    path('update/<int:questionNumber>', views.qandaUpdate, name='qandaUpdate'),

]