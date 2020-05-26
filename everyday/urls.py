from django.urls import path
from . import views

# app_name = 'schedule'

urlpatterns = [
    path('everydayinput', views.everydayinput, name='everydayinput'),
    path('everydaymain', views.everydaymain, name="everydaymain"),
    path('all_events/', views.all_events, name='all_events'),
]
