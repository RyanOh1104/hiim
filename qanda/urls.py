from django.urls import path
from . import views

urlpatterns = [
    # path('qandainput', views.qandainput, name='qandainput'),
    path('qandamain', views.qandamain, name='qandamain'),
    # path('dansangdetail/<int:authuser_id>/<str:slug>', views.dansangdetail, name='dansangdetail'),
    # path('delete/<int:authuser_id>/<str:slug>', views.dansangDelete, name='dansangDelete'),
    # path('update/<int:authuser_id>/<str:slug>', views.dansangUpdate, name='dansangUpdate'),
]