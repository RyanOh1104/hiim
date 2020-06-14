from django.urls import path
from . import views

# app_name = 'schedule'

urlpatterns = [
    path('everydayinput', views.everydayinput, name='everydayinput'),
    path('everydaymain', views.everydaymain, name="everydaymain"),
    path('all_events/', views.all_events, name='all_events'),
    path('everydaydetail/<int:authuser_id>/<str:slug>', views.everydaydetail, name='everydaydetail'),
    path('delete/<int:authuser_id>/<str:slug>', views.delete, name='delete'),
    path('update/<int:authuser_id>/<str:slug>', views.update, name='update'),
]
