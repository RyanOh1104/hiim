from django.urls import path
from . import views

# app_name = 'schedule'

urlpatterns = [
    path('everydaycreate', views.everydayCreate, name='everydaycreate'),
    path('everydaymain', views.everydaymain, name="everydaymain"),
    path('all_events/', views.all_events, name='all_events'),
    path('everydaydetail/<int:authuser_id>/<str:slug>', views.everydayDetail, name='everydaydetail'),
    path('delete/<int:authuser_id>/<str:slug>', views.everydayDelete, name='delete'),
    path('update/<int:authuser_id>/<str:slug>', views.everydayUpdate, name='update'),
]
