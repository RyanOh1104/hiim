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

# 하루하루 기록장 Create page의 view입니다
@login_required(login_url="/register")
def everydayCreate(request):
    today = datetime.today()
    # setting initial user as current logged in user
    form = EverydayInputForm(initial={'authuser':request.user})
    
    if request.method == 'POST':
        form = EverydayInputForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            # authuser에 현재 사용자 저장
            instance.authuser = request.user
            # 날짜 저장
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
            
            # 각 기록의 id 역할을 하는 slug입니다. 저장된 날짜+시간을 slugify해서 저장돼요.
            instance.slug = slugify(today)
            # 각 날짜의 기록에 아래처럼 url을 부여합니다.
            instance.url = "/everydaydetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()

            return redirect('/everyday/everydaymain')

    context = {
        'form' : form,
        'today' : today
    }
    return render(request,'everyday/everyday_create.html', context)

# 하루하루 기록장 Main page의 view입니다
@login_required(login_url="/register")
def everydayMain(request):
    # 현재 로그인 되어있는 유저의 데이터만 query
    todays = NewEvent.objects.filter(authuser=request.user)

    # 현재 로그인 되어있는 유저의 기본정보(UserInfo) query
    thisUser = UserInfo.objects.get(authuser=request.user)

    ########## Main page 상단의 progress bar를 위한 부분입니다. everyday.js로 가져갈 데이터예요 ##########
    getToday = datetime.today()
    # 이번달의 '월'만 가져오는 부분이에요.
    getMonth = getToday.strftime('%m')
    # 이번달에 기록을 남긴 날들을 count합니다.
    countThisMonth = todays.filter(authuser=request.user, when__contains=getMonth).count()
    #####################################################################

    context = {
        'todays' : todays,
        'thisUser' : thisUser,
        'getMonth' : getMonth,
        'countThisMonth' : countThisMonth,
    }
    return render(request,'everyday/everyday_main.html', context)

# 하루하루 Detail page의 view입니다.
@login_required(login_url="/register")
def everydayDetail(request, authuser_id, slug):
    # 각 기록의 slug는 기록의 id처럼 씁니다.
    today = NewEvent.objects.get(slug=slug)

    context = {
        'today' : today,
    }
    return render(request, 'everyday/everyday_detail.html', context)

# 하루하루의 기록을 수정하는 view입니다. Create view와 동일해요. comment처리한 부분만 다릅니다!
@login_required(login_url="/register")
def everydayUpdate(request, authuser_id, slug):
    getToday = NewEvent.objects.get(slug=slug)
    today = datetime.today()

    # 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = EverydayInputForm(request.POST, request.FILES) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user

            ######### 아래를 하지 않았더니, img 필드가 빈 채로 저장되는 현상이 발생했었어요! 왜 그러지.. ##########
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