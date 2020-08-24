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
import json

# Create your views here.
@login_required
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

            #everyday_img = request.FILES.get('img', None) # 원래는 request.FILES['img']인데, 이렇게 하면 파일을 추가하지 않았을 때 에러가 난다.
            # instance.img1 = request.FILES.get('img1')
            # instance.img2 = request.FILES.get('img2')
            # instance.img3 = request.FILES.get('img3')

            if instance.kw1 == "":
                instance.kw1 = "✔️"
            if instance.kw2 == "":
                instance.kw2 = "&nbsp;"
            if instance.kw3 == "":
                instance.kw3 = "&nbsp;"

            if instance.emoji == "":
                instance.emoji = "✔️"

            instance.slug = slugify(today)
            instance.url = "/everydaydetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()

            return redirect('/everyday/everydaymain')

    return render(request,'everyday/everyday_create.html', {'form':form, 'today' : today})

def everydayMain(request):
    todays = NewEvent.objects.filter(authuser=request.user)
    thisUser = UserInfo.objects.get(authuser=request.user)

    getToday = datetime.today()
    getMonth = getToday.strftime('%m')
    countThisMonth = todays.filter(authuser=request.user, when__contains=getMonth).count()
    
    if request.GET:  
        event_arr = []
        all_events = NewEvent.objects.all()

    context = {
        "todays":todays,
        'thisUser':thisUser,
        'getMonth':getMonth,
        'countThisMonth':countThisMonth,
    }
    return render(request,'everyday/everyday_main.html', context)

def all_events(request):
    events = NewEvent.objects.all()
    return HttpResponse(events_to_json(events), content_type='application/json; charset=utf-8')

def everydayDetail(request, authuser_id, slug):
    today = NewEvent.objects.get(slug=slug)
   
    return render(request, 'everyday/everyday_detail.html', {'today' : today})

def everydayUpdate(request, authuser_id, slug):
    getToday = NewEvent.objects.get(slug=slug)
    today = datetime.today()
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = EverydayInputForm(request.POST, request.FILES) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user

            # 아래를 하지 않았더니, img 필드가 텅 빈채로 저장되는 에러(?)가 발생했었다!
            instance.img1 = request.FILES.get('img1')
            instance.img2 = request.FILES.get('img2')
            instance.img3 = request.FILES.get('img3')

            instance.slug = slugify(today)
            instance.url = "/everydaydetail/" + str(authuser_id) + '/' + str(instance.slug)
            getToday.delete()
            instance.save()
            return redirect('/everyday/everydaydetail/' + str(authuser_id) + '/' + str(instance.slug))

    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = EverydayInputForm(instance = getToday)
        return render(request, 'everyday/update.html', {'form':form})

def everydayDelete(request, authuser_id, slug):
    today = NewEvent.objects.get(slug=slug)
    today.delete()
    return redirect('/everyday/everydaymain')