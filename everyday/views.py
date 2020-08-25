from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import EverydayInputForm
from .models import NewEvent
from main.models import UserInfo
from django.forms import modelformset_factory
from datetime import date, datetime
from django.utils import timezone
from django_slugify_processor.text import slugify
from time import strftime
# import json

@login_required
# 하루하루 기록장 Create page의 view입니다
def everydayCreate(request):
    today = datetime.today()
    # setting initial user as current logged in user
    form = EverydayInputForm(initial={'authuser':request.user})
    
    if request.method == 'POST':
        form = EverydayInputForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            instance.when = str(instance.when)

            ########## 여기는 아무 키워드도 입력하지 않았을 때 Main page에 디폴트값을 주기 위한 부분입니다 ##########
            if instance.kw1 == "":
                instance.kw1 = "✔️"
            if instance.kw2 == "":
                instance.kw2 = "&nbsp;"
            if instance.kw3 == "":
                instance.kw3 = "&nbsp;"

            if instance.emoji == "":
                instance.emoji = "✔️"
            ######################################################################################################
            
            # 각 날짜의 기록에 아래처럼 url을 부여합니다.
            # 각 기록의 slug는 저장된 시점을 slugify해서 저장돼요.
            instance.slug = slugify(today)
            instance.url = "/everydaydetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()

            return redirect('/everyday/everydaymain')

    return render(request,'everyday/everyday_create.html', {'form':form, 'today' : today})

# 하루하루 기록장 Main page의 view입니다
def everydayMain(request):
    # 현재 로그인 되어있는 유저의 데이터만 query
    todays = NewEvent.objects.filter(authuser=request.user)
    # 현재 로그인 되어있는 유저의 기본정보(UserInfo) query
    thisUser = UserInfo.objects.get(authuser=request.user)

    # Main page 상단의 progress bar를 위한 부분입니다.
    # everyday.js로 parsing할 데이터를 query하는 부분이에요.
    getToday = datetime.today()
    getMonth = getToday.strftime('%m')
    countThisMonth = todays.filter(authuser=request.user, when__contains=getMonth).count()

    context = {
        'todays' : todays,
        'thisUser' : thisUser,
        'getMonth' : getMonth,
        'countThisMonth' : countThisMonth,
    }
    return render(request,'everyday/everyday_main.html', context)

# 하루하루 Detail page의 view입니다.
def everydayDetail(request, authuser_id, slug):
    # 각 기록의 slug는 기록의 id처럼 씁니다.
    today = NewEvent.objects.get(slug=slug)
   
    return render(request, 'everyday/everyday_detail.html', {'today' : today})

# 하루하루의 기록을 수정하는 view입니다.
def everydayUpdate(request, authuser_id, slug):
    # 해당 날짜의 기록을 query.
    getToday = NewEvent.objects.get(slug=slug)
    # 새로운 slug(id)를 부여하기 위해 가져옵니다
    today = datetime.today()

    # 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = EverydayInputForm(request.POST, request.FILES) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user

            ######### 아래를 하지 않았더니, img 필드가 텅 빈채로 저장되는 현상이 발생했었어요! 왜 그러지.. ##########
            instance.img1 = request.FILES.get('img1')
            instance.img2 = request.FILES.get('img2')
            instance.img3 = request.FILES.get('img3')
            #####################################################################################################

            instance.slug = slugify(today)
            instance.url = "/everydaydetail/" + str(authuser_id) + '/' + str(instance.slug)

            # 기존에 있던 건 지워버립니다.
            getToday.delete()
            instance.save()
            return redirect('/everyday/everydaydetail/' + str(authuser_id) + '/' + str(instance.slug))

    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        # 해당 날짜에 해당하는 instance를 가져옵니다.
        form = EverydayInputForm(instance = getToday)
        return render(request, 'everyday/update.html', {'form':form})

# 하루하루의 기록을 지우는 view입니다.
def everydayDelete(request, authuser_id, slug):
    today = NewEvent.objects.get(slug=slug)
    today.delete()
    return redirect('/everyday/everydaymain')