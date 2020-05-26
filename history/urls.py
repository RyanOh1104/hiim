from django.urls import path
from . import views

urlpatterns = [
    path('historyinput', views.historyinput, name='historyinput'),
    path('historymain', views.historymain, name='historymain'),
    path('historydetail/<int:authuser_id>/<slug:slug>', views.historydetail, name="historydetail")
]