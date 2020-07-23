from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import DansangInputForm
from .models import DansangInput, DansangSeed, SeedCategory, SeedCategoryEng
from django.utils import timezone
from datetime import datetime, date
from django_slugify_processor.text import slugify
from django.db.models import F

@login_required
def dansanginput(request):
    today = datetime.today()
    # setting initial user as current logged in user
    form = DansangInputForm(initial={'authuser':request.user})

    if request.method == 'POST':
        form = DansangInputForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            
            instance.img= request.FILES.get('img')
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

@login_required
def dansangmain(request):
    dansangs = DansangInput.objects.filter(authuser=request.user).order_by('created')
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
    seeds = DansangSeed.objects.all().order_by('-datePosted')
    categories = SeedCategory.objects.all()
    categoriesInEng = SeedCategoryEng.objects.all()
    context = {
        'seeds':seeds,
        'categories' : categories,
        'categoriesInEng':categoriesInEng,
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

def add_click(request):
    thisId = request.GET.get("seedId", None)
    thisSeed = DansangSeed.objects.get(pk=thisId)
    thisSeed.clicks = F('clicks') + 1
    thisSeed.save()

    return HttpResponse()   # 이건 솔직히 왜 해야하는지 모르겠음. 근데 아무것도 안해주면 it returned None instead라는 에러 뜸.

def error404(request):
    return render(request, "404.html", status=404)

def error500(request):
    return render(request, "500.html", status=500)


'''
from django.http import (
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseForbidden,
)
from django.shortcuts import render
from django_summernote.settings import summernote_config, get_attachment_model
from django.utils.translation import ugettext_lazy as _
def editor(request, id):
    return render(
        request,
        'django_summernote/widget_iframe_editor.html',
        {
            'id_src': id,
            'id': id.replace('-', '_'),
            'css': (
                summernote_config['default_css'] +
                summernote_config['css']
            ),
            'js': (
                summernote_config['default_js'] +
                summernote_config['js']
            ),
            'disable_upload': summernote_config['disable_upload'],
        }
    )
def upload_attachment(request):
    if request.method != 'POST':
        return HttpResponseBadRequest(_('Only POST method is allowed'))
    if summernote_config['attachment_require_authentication']:
        if not request.user.is_authenticated():
            return HttpResponseForbidden(_('Only authenticated users are allowed'))
    if not request.FILES.getlist('files'):
        return HttpResponseBadRequest(_('No files were requested'))

    # remove unnecessary CSRF token, if found
    kwargs = request.POST.copy()
    kwargs.pop("csrfmiddlewaretoken", None)

    try:
        attachments = []

        for file in request.FILES.getlist('files'):
            # create instance of appropriate attachment class
            klass = get_attachment_model()
            attachment = klass()
            attachment.file = file
            attachment.name = file.name
            if file.size > summernote_config['attachment_filesize_limit']:
                return HttpResponseBadRequest(
                    _('File size exceeds the limit allowed and cannot be saved')
                )

            # calling save method with attachment parameters as kwargs
            attachment.save(**kwargs)

            attachments.append(attachment)
        return render(request, 'django_summernote/upload_attachment.json', {
            'attachments': attachments,
        })
    except IOError:
        return HttpResponseServerError(_('Failed to save attachment'))
'''

