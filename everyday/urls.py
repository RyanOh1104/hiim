from django.urls import path
from . import views

urlpatterns = [
    path('everydaycreate', views.everydayCreate, name='everydaycreate'),
    path('everydaymain', views.everydayMain, name="everydaymain"),
    path('everydaydetail/<int:authuser_id>/<str:slug>', views.everydayDetail, name='everydaydetail'),
    path('delete/<int:authuser_id>/<str:slug>', views.everydayDelete, name='delete'),
    path('update/<int:authuser_id>/<str:slug>', views.everydayUpdate, name='update'),
]
