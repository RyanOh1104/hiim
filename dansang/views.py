from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import DansangInputForm
from .models import DansangInput, DansangSeed, SeedCategory
from django.utils import timezone
from datetime import datetime, date
from django_slugify_processor.text import slugify
### 아래는 씨앗 조회수 확인을 위해 ###
# from django.shortcuts import get_object_or_404
# from django.views.generic.base import RedirectView
# from .models import DansangSeed

@login_required
def dansanginput(request):
    # setting initial user as current logged in user
    today = datetime.today()
    form = DansangInputForm(initial={'authuser':request.user})
    if request.method == 'POST':
        form = DansangInputForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            
            instance.created = str(today)
            # main에서 제목 display
            if len(instance.title) >= 17:
                instance.title = instance.title[0:17] + "..."
            # main에서 부제목 display -- subtitle OR first_sentence
            if len(instance.subtitle) >= 35:
                instance.subtitle = instance.subtitle[0:35] + "..."
            # Subtitle이 없다면 First Sentence로 대체
            # PROBLEM : 첫문장이 짧고, 그 다음에 줄바꿈을 하면 그 줄바꿈(tag)이 그대로 subtitle에 반영된다.
            # 즉, subtitle이 없는 경우 contents의 첫 부분을 가져오는데 문제는 html tag가 모두 포함된다는 것.
            if instance.subtitle == "":
                instance.first_sentence = instance.contents[0:35] + "..."
                instance.subtitle = instance.first_sentence

            instance.slug = slugify(datetime.now())
            # instance.slug = slugify(instance.title, allow_unicode=True)   이건 한글 제목일 때 불가능!
            instance.url = "/dansang/dansangdetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
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

def seed(request):
    seed = DansangSeed.objects.all()
    category = SeedCategory.objects.all()
    context = {
        'seeds':seeds
        'categories' : categories
    }
    return render(request, 'dansang/seed.html', context)

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

            # main에서 제목 display
            if len(instance.title) >= 17:
                instance.title = instance.title[0:17] + "..."
            # main에서 부제목 display -- subtitle OR first_sentence
            if len(instance.subtitle) >= 35:
                instance.subtitle = instance.subtitle[0:35] + "..."
            # Subtitle이 없다면 First Sentence로 대체
            # PROBLEM : 첫문장이 짧고, 그 다음에 줄바꿈을 하면 그 줄바꿈(tag)이 그대로 subtitle에 반영된다.
            # 즉, subtitle이 없는 경우 contents의 첫 부분을 가져오는데 문제는 html tag가 모두 포함된다는 것.
            if instance.subtitle == "":
                instance.subtitle = "&nbsp;"

            instance.created = thisDansang.created
            instance.slug = slugify(datetime.now())
            instance.url = "/dansang/dansangdetail/" + str(authuser_id) + '/' + str(instance.slug)
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

def error404(request):
    return render(request, "404.html", status=404)

def error500(request):
    return render(request, "500.html", status=500)

### 씨앗 조회수 세기 ###
# class ArticleCounterRedirectView(RedirectView):
#     permanent = False
#     query_string = True

#     def get_redirect_url(self, *args, **kwargs):
#         article = get_object_or_404(Article, pk=kwargs['pk'])
#         article.update_counter()
#         return article.url


