"""mvp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from register import views as v
# from django.conf.urls import url, handler404, handler500

# handler404 = "chatbot_app.views.error404"
# handler500 = "chatbot_app.views.error500"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('register/', v.register, name='register'),
    path('', include("django.contrib.auth.urls")),   # Django의 로그인/로그아웃을 위한 built-in 페이지
    path('dansang/', include('dansang.urls')),
    path('everyday/', include('everyday.urls')),
    path('history/', include('history.urls')),
    path('summernote/', include('django_summernote.urls')),
]
