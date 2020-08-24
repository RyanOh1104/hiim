from django.urls import path
from . import views

urlpatterns = [
    # path('<int:id>', views.index, name='index'),    
    # <int:id>는 id로 찾는 것. id라는 integer를 받고, 이걸 views.index로 pass. 즉, 그러므로 views.index에 'id'라는 parameter를 추가해줘야겠지?
    path('dansangcreate', views.dansangCreate, name='dansanginput'),
    path('dansangmain', views.dansangmain, name='dansangmain'),
    path('dansangdetail/<int:authuser_id>/<str:slug>', views.dansangDetail, name='dansangdetail'),
    path('delete/<int:authuser_id>/<str:slug>', views.dansangDelete, name='dansangDelete'),
    path('update/<int:authuser_id>/<str:slug>', views.dansangUpdate, name='dansangUpdate'),
    path('seed', views.seed, name='seed'),
    path('seed/<str:category>', views.seedByCat, name='seedByCat'),
    path('ajax/add_click', views.add_click, name="add_click"),

]