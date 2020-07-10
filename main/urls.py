from django.urls import path
from main import views

urlpatterns = [
    # path('<int:id>', views.index, name='index'),    
    # <int:id>는 id로 찾는 것. id라는 integer를 받고, 이걸 views.index로 pass. 즉, 그러므로 views.index에 'id'라는 parameter를 추가해줘야겠지?
    # path('', views.home, name="home"),
    # path('create/', views.create, name='create'),
    # path('view/', views.view, name="view")
    path('inputuserinfo', views.inputuserinfo, name='inputuserinfo'),
    path('', views.usermain, name='usermain'),
    path('welcome', views.landing, name="landing"),
    path('hiim', views.hiim, name="hiim"),
    path('tong', views.tong, name='tong'),
    path('update/<int:authuser_id>', views.update, name='update'),
]

# from .views import ArticleCounterRedirectView, ArticleDetail

# urlpatterns = [
#     path('counter/<int:pk>/', ArticleCounterRedirectView.as_view(), name='article-counter'),
# ]