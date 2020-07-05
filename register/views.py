from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, auth     

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
                return redirect('/inputuserinfo')

            # 여기에 새로 가입한 user의 id를 어떤 변수에 받아오고, 그걸 아래에 뒤에 <int:id>처럼 붙이면 어떨까? 바로 자기 페이지로 redirect되게.
    else:
        form = RegisterForm()

        a = form.fields['username']
        a.label = "아이디"
        a.help_text = "영문자+숫자 조합!" 

        b = form.fields['email']
        b.label = "이메일"

        c = form.fields['password1']
        c.label = "비밀번호"
        c.help_text = "영문자+숫자 조합으로 8자 이상 입력해주세요! (특수문자 불가)" 

        d = form.fields['password2']
        d.label = "비밀번호 확인"
        d.help_text = "실수하지 말고(!) 한번 더 입력해주세요!" 

    return render(response, 'register/register.html', {'form' : form}) 
