from django.urls import path
from main import views

urlpatterns = [
    path('inputuserinfo', views.inputuserinfo, name='inputuserinfo'),
    path('', views.usermain, name='usermain'),
    path('welcome', views.landing, name="landing"),
    path('hiim', views.hiim, name="hiim"),
    path('tong', views.tong, name='tong'),
    path('update/<int:authuser_id>', views.update, name='update'),
]