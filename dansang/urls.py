from django.urls import path
from . import views

urlpatterns = [
    # path('<int:id>', views.index, name='index'),    
    # <int:id>는 id로 찾는 것. id라는 integer를 받고, 이걸 views.index로 pass. 즉, 그러므로 views.index에 'id'라는 parameter를 추가해줘야겠지?
    path('dansanginput', views.dansanginput, name='dansanginput'),
    path('dansangmain', views.dansangmain, name='dansangmain'),
    path('dansangdetail/<int:authuser_id>/<str:slug>', views.dansangdetail, name='dansangdetail'),
    path('delete/<int:authuser_id>/<str:slug>', views.dansangDelete, name='dansangDelete'),
    path('update/<int:authuser_id>/<str:slug>', views.dansangUpdate, name='dansangUpdate'),
    path('dailyinputs/<int:num>', views.dailyinputs, name='dailyinputs'),

]