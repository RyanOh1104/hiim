from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import InputUserForm
from django.contrib.auth.models import User
from .models import UserInfo
from dansang.models import DansangSeed, DansangInput
from everyday.models import NewEvent
from qanda.models import Answer
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth import login, authenticate
# 이건 왜 넣었는지 기억이 안나네요...!
from django.contrib.auth.forms import UserCreationForm    

@login_required(login_url="/register")
def inputUserinfo(response):
    if response.method == 'POST':
        form = InputUserForm(response.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            # authuser에 현재 로그인된 사용자 저장
            instance.authuser = response.user
            instance.save()
        return HttpResponseRedirect('/')
    else:
            form = InputUserForm()
    
    context = {
        'form' : form,
    }
    return render(response, 'main/inputuserinfo.html', context)


def usermain(request):
    today = date.today()

    # 계정이 있다면
    if request.user.is_authenticated:
        current_user = request.user
        # 계정이 있고, 사용자정보(Userinfo)도 입력했다면
        if UserInfo.objects.filter(authuser_id=current_user.id).exists():
            thisUser = UserInfo.objects.get(authuser_id=current_user.id)

            ########## 아래는 새로운 씨앗이 등록되었는지 확인하기 위한 부분입니다. 씨앗은 지금 중요하지 않으니 패쓰!! ##########
            # 오늘 날짜의 씨앗이 있으면 가져오고, 없으면 none을 가져와요
            newSeed = DansangSeed.objects.filter(datePosted=today).first()
            ###############################################################################################################

            # 각 기록장에 저장된 기록의 수를 가져오는 query입니다. 
            thisUserDansang = DansangInput.objects.filter(authuser=request.user).count()
            thisUserEveryday = NewEvent.objects.filter(authuser=request.user).count()
            thisUserQanda = Answer.objects.filter(authuser=request.user).count()

            context = {
                'thisUser' : thisUser,
                'newSeed' : newSeed,
                'thisUserDansang' : thisUserDansang,
                'thisUserEveryday' : thisUserEveryday,
                'thisUserQanda' : thisUserQanda,
            }
            return render(request, 'main/usermain.html', context)

        # 계정은 있는데 사용자정보(UserInfo)를 입력하지 않았다면
        else: 
            return redirect('/inputUserinfo')

    # 계정도 없을 때
    else:
        return redirect('/register')

# 사용자정보(UserInfo)를 수정하는 페이지입니다. inputUserinfo와 동일해요. comment처리한 부분만 다릅니다!
def updateUserinfo(response, authuser_id):
    thisUser = UserInfo.objects.get(authuser_id = authuser_id)
    if response.method == "POST":
        form = InputUserForm(response.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.authuser = thisUser.authuser

            # 기존에 있던 thisUser를 delete해주지 않으면 고유값인 authuser_id의 충돌이 일어나므로 저장 전에 제거해줍니다.
            thisUser.delete()   
            instance.save()
        return HttpResponseRedirect('/')

    # 수정하기 위해 페이지에 들어왔을 때
    else: 
        # 현재 로그인된 유저의 UserInfo form을 가져와요.
        form = InputUserForm(instance = thisUser)
        context = {
            'form' : form
        }
        return render(response, 'main/inputuserinfo.html', context)

########## 아래 두 view는 각각 랜딩 페이지와 소개 페이지에요. 추후 보완할 예정이니 일단 무시해주세요! ##########
def landing(request):
    return render(request, 'main/landing.html')

def hiim(request):
    if request.user.is_authenticated:
        current_user = request.user
        thisUser = UserInfo.objects.get(authuser_id=current_user.id)
        
        return render(request, 'main/hiim.html', {'thisUser':thisUser})
    else: 
        return redirect('/')

# 텅 빈 페이지 - 재미로 만들어봤어요.. 무시해주세요..
def tong(request):
    return render(request, 'main/tong.html')