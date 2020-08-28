from django.urls import path
from . import views

urlpatterns = [
    path('dansangcreate', views.dansangCreate, name='dansangcreate'),
    path('dansangmain', views.dansangMain, name='dansangmain'),
    path('dansangdetail/<int:authuser_id>/<str:slug>', views.dansangDetail, name='dansangdetail'),
    path('delete/<int:authuser_id>/<str:slug>', views.dansangDelete, name='dansangDelete'),
    path('update/<int:authuser_id>/<str:slug>', views.dansangUpdate, name='dansangUpdate'),

    ########### 여기부터는 '씨앗'에 관련된 부분입니다. 일단 무시해주세요! ##########
    path('seed', views.seed, name='seed'),
    path('seed/<str:category>', views.seedByCat, name='seedByCat'),
    path('ajax/add_click', views.add_click, name="add_click"),
]