from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, auth    
from time import sleep 

# Create your views here. 
def register(response):
    if response.method == 'POST':
        # form = UserCreationForm(response.POST)      # UserCreationForm 대신 내가 직접 만든 RegisterForm을 쓸 것이므로 지우기
        form = RegisterForm(response.POST)
        if form.is_valid:
            form.save()
            # 아래는 auto login을 위한 code
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            newUser =  authenticate(response, username=username, password=password)
            if newUser:
                login(response, newUser)
                print('logged in!')
                sleep(3)
                return redirect('/inputuserinfo')
            else:
                return redirect('/register')

    else:
        form = RegisterForm()

        a = form.fields['username']
        a.label = "아이디"
        a.help_text = "영문자+숫자 조합!" 

        b = form.fields['email']
        b.label = "이메일"

        c = form.fields['password1']
        c.label = "비밀번호"
        c.help_text = "영문자+숫자 조합으로 8자 이상 입력해주세요!<br>+ 아이디와 비슷하면 등록되지 않아요!" 

        d = form.fields['password2']
        d.label = "비밀번호 확인"
        d.help_text = "실수하지 말고(!) 한번 더 입력해주세요!" 

    return render(response, 'register/register.html', {'form' : form}) 
