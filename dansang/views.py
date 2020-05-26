from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import DansangInputForm
from .models import DansangInput, DansangSource
from django.utils import timezone
import datetime
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
            # Title 자르기
            if len(instance.title) >= 17:
                instance.title = instance.title[0:17] + "..."
            # Subtitle 자르기
            if len(instance.subtitle) >= 35:
                instance.subtitle = instance.subtitle[0:35] + "..."
            # First Sentence 자르기
            if len(instance.contents) >= 35:
                instance.first_sentence = instance.contents[0:35] + "..."
            # Subtitle이 없다면 First Sentence로 대체
            if instance.subtitle == "":
                instance.subtitle = instance.first_sentence
            instance.slug = slugify(datetime.datetime.now())
            # instance.slug = slugify(instance.title, allow_unicode=True)   이건 한글 제목일 때 불가능!
            # instance.save()   이거는 url의 마지막을 이 dansang의 id로 쓰고자 할 때 활성화. 
            instance.url = "127.0.0.1:8000/dansang/dansangdetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()
            return redirect('/dansang/dansangmain')

    return render(request,'dansang/dansanginput.html',{'form':form})


def dansangmain(request):
    dansangs = DansangInput.objects.filter(authuser=request.user)
    how_many = dansangs.count()

    # today = date.today()
    # sources = DansangSource.objects.get()

    return render(request, 'dansang/dansangmain.html', {'dansangs' : dansangs, 'how_many':how_many})

def dansangdetail(request, authuser_id, slug):
    thisDansang = DansangInput.objects.get(slug=slug)
    if thisDansang.created == thisDansang.modified:
        thisDansang.modified = '' 
    return render(request, 'dansang/dansangdetail.html', {'thisDansang' : thisDansang})



