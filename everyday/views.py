from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import EverydayInputForm, EverydayImageForm
from .models import NewEvent, EverydayImage
from main.models import UserInfo
from django.forms import modelformset_factory
from datetime import date, datetime
from django.utils import timezone
from django_slugify_processor.text import slugify
import json

# Create your views here.
@login_required
def everydayinput(request):
    today = datetime.today()
    # setting initial user as current logged in user
    form = EverydayInputForm(initial={'authuser':request.user})
    ImageFormSet = modelformset_factory(EverydayImage, form=EverydayImageForm, extra=3)
    formset = ImageFormSet(queryset=EverydayImage.objects.none())
    if request.method == 'POST':
        form = EverydayInputForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=EverydayImage.objects.none())
        
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            instance.when = str(instance.when)

            #everyday_img = request.FILES.get('img', None) # 원래는 request.FILES['img']인데, 이렇게 하면 파일을 추가하지 않았을 때 에러가 난다.
            # instance.img= request.FILES.get('img')
            if instance.kw1 == "":
                instance.kw1 = "&nbsp;"
            if instance.kw2 == "":
                instance.kw2 = "&nbsp;"
            if instance.kw3 == "":
                instance.kw3 = "&nbsp;"

            instance.slug = slugify(today)
            instance.url = "/everydaydetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()

            for img_form in formset.cleaned_data:
            # 유저가 모든 이미지들을 업로드하지 않았을 경우 crash 방지
                if img_form:
                    image = img_form['image']
                    photo = EverydayImage(other_contents=form, image=image)
                    photo.save()

            return redirect('/everyday/everydaymain')

    return render(request,'everyday/everydayinput.html', {'form':form, 'today' : today, 'formset':formset})

def everydaymain(request):
    all_events = NewEvent.objects.filter(authuser=request.user)
    thisUser = UserInfo.objects.get(authuser=request.user)
    if request.GET:  
        event_arr = []
        all_events = NewEvent.objects.all()

    context = {
        "todays":all_events,
        'thisUser':thisUser
    }
    return render(request,'everyday/everydaymain.html', context)

def all_events(request):
    events = NewEvent.objects.all()
    return HttpResponse(events_to_json(events), content_type='application/json; charset=utf-8')

def everydaydetail(request, authuser_id, slug):
    today = NewEvent.objects.get(slug=slug)
    return render(request, 'everyday/everydaydetail.html', {'today' : today})

def everydayUpdate(request, authuser_id, slug):
    # thisDansang = DansangInput.objects.get(slug=slug)
    # form = DansangInputForm(instance=thisDansang)
    # return render(request, 'dansang/dansangmain.html', {'form':form})
    getToday = NewEvent.objects.get(slug=slug)
    today = datetime.today()
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = EverydayInputForm(request.POST) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
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