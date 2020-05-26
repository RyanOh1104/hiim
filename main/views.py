from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import InputUserForm
from .models import UserInfo
# 아래 두개는 굳이 필요한 건지는 모르겠음
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm    
from django.contrib.auth.decorators import login_required


@login_required(login_url="/register")
# Create your views here. 
def inputuserinfo(response):
    if response.method == 'POST':
        form = InputUserForm(response.POST)
        if form.is_valid:
            # 아래는 ForeignKey인 authuser에 이 form을 입력한 user를 저장하는 코드.
            instance = form.save(commit=False)
            instance.authuser = response.user
            instance.save()
#################### 새로운 ToDoList를 추가하는 부분. 근데 UserInfo는 뭘 추가하는 게 아니라, 미리 입력받은 걸 보여주는 것
            # n = form.cleaned_data["name"]      
            # t = ToDoList(name=n)              # 새로 만들어진 ToDoList의 이름이 n이다.
            # t.save()                           
            # Now, below is about user-specific ToDoList. 이제 list를 만들고 바로 저장하는 게 아니라, user에게 저장해야 한다.
            # response.user.todolist.add(t)
        # return HttpResponseRedirect("/%i" %t.id)
#################### 
        return HttpResponseRedirect('/main/usermain')
        # response, "main/usermain.html", {}) <-- 이게 아니고 위에가 맞다. 흠 왜그럴까?
    else:
        form = InputUserForm()

    return render(response, 'main/inputuserinfo.html', {'form':form})

def usermain(request):
    thisUser = UserInfo.objects.get(authuser=request.user)

    return render(request, 'main/usermain.html', {'thisUser' : thisUser}) # 여기 세번째 패라미터는 저 user를 template에 담아내기 위한 것.

