from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import HistoryInputForm
from .models import HistoryInput
from main.models import UserInfo
from django.utils import timezone
import datetime
from django_slugify_processor.text import slugify

# Create your views here.
@login_required
def historyinput(request):
    form = HistoryInputForm(initial={'authuser':request.user})

    if request.method == 'POST':
        form = HistoryInputForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            if instance.end_date != None:
                temp = str(instance.end_date).split("-")    # temp = ['1994', '01', '04']
                temp2 = [temp[0], temp[1], temp[2]]
                i = 1
                while i < 3:
                    thisDate = list(temp[i])
                    if thisDate[0] == '0':   # ['0', '1']
                        thisDate.remove('0')    #['1']
                        temp2[i] = thisDate[0]
                        i = i + 1
                instance.end = str(temp2[0] + '년 ' + temp2[1] + '월 ' + temp2[2] + '일')
            elif instance.end_date == None:
                instance.end = instance.end_ing
            instance.slug = slugify(datetime.datetime.now())
            instance.url = "127.0.0.1:8000/history/historydetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            instance.save()
            return redirect('/history/historymain')
    
    return render(request, 'history/historyinput.html', {'form':form})

def historymain(request):
    thisUser = UserInfo.objects.get(authuser=request.user)
    objects = HistoryInput.objects.all()

    return render(request, 'history/historymain.html', {'thisUser' : thisUser, 'objects':objects}) 

def historydetail(request, authuser_id, slug):
    #여기서 what 대신 쓸 게 필요하다. like slug
    thisHistory = HistoryInput.objects.get(slug=slug)

    return render(request, 'history/historydetail.html', {'thisHistory' : thisHistory})