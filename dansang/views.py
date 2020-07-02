from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import DansangInputForm
from .models import DansangInput, DansangSource
from django.utils import timezone
from datetime import datetime, date
from django_slugify_processor.text import slugify

@login_required
def dansanginput(request):
    # setting initial user as current logged in user
    form = DansangInputForm(initial={'authuser':request.user})
    if request.method == 'POST':
        form = DansangInputForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            
            if len(instance.title) >= 17:
                instance.title = instance.title[0:17] + "..."
            if len(instance.subtitle) >= 35:
                instance.subtitle = instance.subtitle[0:35] + "..."
            if len(instance.contents) >= 35:
                instance.first_sentence = instance.contents[0:35] + "..."
                
            # Subtitle이 없다면 First Sentence로 대체
            if instance.subtitle == "":
                instance.subtitle = instance.first_sentence
            instance.slug = slugify(datetime.now())
            # instance.slug = slugify(instance.title, allow_unicode=True)   이건 한글 제목일 때 불가능!
            # instance.save()   이거는 url의 마지막을 이 dansang의 id로 쓰고자 할 때 활성화. 
            instance.url = "/dansangdetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()
            return redirect('/dansang/dansangmain')

    return render(request,'dansang/dansanginput.html', {'form':form})


def dansangmain(request):
    dansangs = DansangInput.objects.filter(authuser=request.user)
    how_many = dansangs.count()
    today = date.today() # doen't work FUCK... 왜 2020년%206월%2011일??????
    context = {
        'dansangs': dansangs,
        'how_many': how_many,
        'today': today
    }

    return render(request, 'dansang/dansangmain.html', context)

def dansangdetail(request, authuser_id, slug):
    thisDansang = DansangInput.objects.get(slug=slug)
    if thisDansang.created == thisDansang.modified:
        thisDansang.modified = '' 
    return render(request, 'dansang/dansangdetail.html', {'thisDansang' : thisDansang})

def dailyinputs(request, num):
    today = date.today()
    context = {

    }
    return render(request, 'dansang/dailyinputs.html', context)

def dansangUpdate(request, authuser_id, slug):
    # thisDansang = DansangInput.objects.get(slug=slug)
    # form = DansangInputForm(instance=thisDansang)
    # return render(request, 'dansang/dansangmain.html', {'form':form})
    thisDansang = DansangInput.objects.get(slug=slug)
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = DansangInputForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            instance.slug = slugify(datetime.now())
            instance.url = "/dansangdetail/" + str(authuser_id) + '/' + str(instance.slug)
            thisDansang.delete()
            instance.save()
            return redirect('/dansang/dansangdetail/' + str(authuser_id) + '/' + str(instance.slug))

    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = DansangInputForm(instance = thisDansang)
        return render(request, 'dansang/update.html', {'form':form})

def dansangDelete(request, authuser_id, slug):
    thisDansang = DansangInput.objects.get(slug=slug)
    thisDansang.delete()
    return redirect('/dansang/dansangmain')



