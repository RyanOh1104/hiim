from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import InputUserForm
from .models import UserInfo
# 아래 두개는 굳이 필요한 건지는 모르겠음
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm    
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
# Create your views here. 
def inputuserinfo(response):
    if response.method == 'POST':
        form = InputUserForm(response.POST)
        if form.is_valid:
            # 아래는 ForeignKey인 authuser에 이 form을 입력한 user를 저장하는 코드.
            instance = form.save(commit=False)
            instance.authuser = response.user
            instance.save()
        return HttpResponseRedirect('/')
        # response, "main/usermain.html", {}) <-- 이게 아니고 위에가 맞다. 흠 왜그럴까?
    else:
        form = InputUserForm()

    return render(response, 'main/inputuserinfo.html', {'form':form})

def update(response, authuser_id):
    thisUser = UserInfo.objects.get(authuser_id = authuser_id)
    if response.method == "POST":
        form = InputUserForm(response.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.authuser = thisUser.authuser
            thisUser.delete()   # 기존에 있던 thisUser를 delete해주지 않으면 고유값인 authuser_id의 충돌이 일어난다.
            instance.save()
        return HttpResponseRedirect('/')
    else: 
        form = InputUserForm(instance = thisUser)
        return render(response, 'main/inputuserinfo.html', {'form':form})

@login_required(login_url="/welcome")
def usermain(request):
    thisUser = UserInfo.objects.get(authuser=request.user)

    return render(request, 'main/usermain.html', {'thisUser' : thisUser}) # 여기 세번째 패라미터는 저 user를 template에 담아내기 위한 것.

def landing(request):
    # return HttpResponseRedirect('/main/landing')
    return render(request, 'main/landing.html')

def hiim(request):
    # return HttpResponseRedirect('/main/landing')
    return render(request, 'main/hiim.html')

def tong(request):
    return render(request, 'main/tong.html')