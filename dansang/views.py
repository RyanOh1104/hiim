from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import DansangInputForm
from .models import DansangInput, DansangSeed, SeedCategory, SeedCategoryEng
from django.utils import timezone
from datetime import datetime, date
from django_slugify_processor.text import slugify
from django.core.paginator import Paginator
from django.db.models import F
from django.utils.html import strip_tags
from mvp.korengtrans import trans

# 끄적끄적의 Create view
@login_required
def dansangCreate(request):
    today = timezone.now()
    # setting initial user as current logged in user
    form = DansangInputForm(initial={'authuser':request.user})

    ########## 각 글을 사용자가 카테고라이징을 할 수 있도록 하는 부분인데, 당장은 중요하지 않으니 패쓰! ##########
    categoryList = list(DansangInput.objects.filter(authuser=request.user).values_list('category', flat=True).distinct())
    indexList = [*range(1, len(categoryList)+1, 1)] # range 앞에 *을 붙이는 이유는, 저걸 없애면 range()를 알아먹지 못한다.
    # 이제 이걸 [{index: category}, {index: category}, {index: category}, ...]의 꼴로 만들어야 한다.
    categories = []
    for i in range(0,len(categoryList)):
        catDict = {}
        catDict[indexList[i]] = categoryList[i]
        categories.append(catDict)
    ##########################################################################################################

    # 사용자가 글을 저장할 때
    if request.method == 'POST':
        form = DansangInputForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            # authuser를 현재 로그인되어있는 사용자로
            instance.authuser = request.user
            # 사용자가 이미지를 첨부했을 때, 이미지 저장
            instance.img= request.FILES.get('img')
            # 글을 쓴 날짜 = 오늘 날짜
            instance.created = str(today)

            # strip tags - 제목과 부제목에 입혀진 html tag를 벗겨내는 부분이에요.
            title_stripped = strip_tags(instance.title)
            subtitle_stripped = strip_tags(instance.subtitle)

            ########## Main page에서 제목과 부제목이 보여질텐데, 길이가 길면 다음줄로 넘어가기 때문에 적정선에서 잘라주는 부분입니다. ##########
            # Main에서 제목 display
            if len(title_stripped) >= 17:
                instance.title = title_stripped[0:17] + "..."
            else:
                instance.title = title_stripped

            # main에서 부제목 display
            if len(subtitle_stripped) >= 35:
                instance.subtitle = subtitle_stripped[0:35] + "..."
            else:
                instance.subtitle = subtitle_stripped

            # Subtitle이 없다면,
            # 원래는 본문의 첫부분을 가져와 대체하려고 했는데, 일단 보류하고 공백으로 대체!
            if instance.subtitle == "":
                # contents_stripped = strip_tags(instance.contents)
                # instance.subtitle = contents_stripped[0:30] + "..."
                instance.subtitle = "&nbsp;"
            ###############################################################################################################################

            # 사용자가 입력한 카테고리를 영문으로 변경하는 부분입니다.
            catByUser = instance.category
            instance.categoryEng = trans(catByUser)

            # Slug는 각 글의 id처럼 쓰입니다.
            # 글이 쓰여진 날짜+시간을 slug 형태로 만들어 저장해요!
            instance.slug = slugify(datetime.now())
            # 글의 주소인 url은 authuser_id와 url로 만들어 저장합니다.
            instance.url = "/dansang/dansangdetail/" + str(instance.authuser_id) + '/' + str(instance.slug)
            # 최종적으로 저장해줍니다.
            instance.save()
            return redirect('/dansang/dansangmain')

    context = {
        'form' : form,
        'categories' : categories
    }
    return render(request,'dansang/dansang_create.html', context)

@login_required
def dansangMain(request):
    dansangs = DansangInput.objects.filter(authuser=request.user).order_by('-created')
    how_many = dansangs.count()

    categoryList = list(DansangInput.objects.filter(authuser=request.user).values_list('category', flat=True).distinct())
    
    # 요 부분은 임시적으로! 태건이 끝나면 바로 제거
    # categoryEngList = []
    # for k in range(0,len(categoryList)):
    #     categoryEngList.append(trans(categoryList[k]))
    
    categoryEngList = list(DansangInput.objects.filter(authuser=request.user).values_list('categoryEng', flat=True).distinct())
    indexList = [*range(1, len(categoryList)+1, 1)] # range 앞에 *을 붙이는 이유는, 저걸 없애면 range()를 알아먹지 못한다.
    
    indexLength = len(indexList)
    # indexList는 integer이기 때문에 모두 string으로 바꿔줘야 한다. 
    for a in range(0, indexLength):
        indexList[a] = str(indexList[a])

    # 이제 이걸 [{index: category}, {index: category}, {index: category}, ...]의 꼴로 만들어야 해
    categories = []
    for i in range(0,len(categoryList)):
        catDict = {}
        catDict[indexList[i]] = categoryList[i]
        categories.append(catDict)
    
    '''
    categories = []
    for i in range(0, len(categoryList)):
        catDict = {}
        catDict[categoryEngList[i]] = categoryList[i]
        categories.append(catDict)
    '''
    # pagination
    dansangPaginator = Paginator(dansangs, 7)
    page = request.GET.get('page')
    posts = dansangPaginator.get_page(page)

    context = {
        'dansangs': dansangs,
        'how_many': how_many,
        # 'today': today,
        'posts':posts,
        'categoryList':categoryList,
        'categories':categories,
        'categoryList':categoryList,
        'categoryEngList': categoryEngList,
        'indexList': indexList,
        'indexLengthRange':range(1, indexLength+1),

    }

    return render(request, 'dansang/dansang_main.html', context)

def dansangDetail(request, authuser_id, slug):
    thisDansang = DansangInput.objects.get(slug=slug)

    return render(request, 'dansang/dansang_detail.html', {'thisDansang' : thisDansang})

# 이건 login_required 굳이 필요 없으려나?
def seed(request):
    seeds = DansangSeed.objects.all().order_by('-datePosted')
    categories = SeedCategory.objects.all()
    categoriesInEng = SeedCategoryEng.objects.all()

    # 'New' 딱지 붙일 씨앗 -- datePosted가 max인 것 찾기
    latestDatePosted = DansangSeed.objects.all().values('datePosted')
    # allDates의 각 원소는 {'dateAnswered':datetime.date(2020, 07, 21)} 이런 포맷 (python dictionary view)
    allDates = list(latestDatePosted.values('datePosted'))
    # Date 중 최댓값, 즉 가장 최근의 질문의 날짜 가져오기 (바로 위와 정확히 동일)
    datesList = []
    datesListInFormat = []
    for j in range(0, len(allDates)): # !!!!!! 대체 왜 len()-1이 아닌지 모르겠다!!!!!!
        datesList.append(*allDates[j].values()) # 각 원소는 datetime.date(2020,07,21)의 포맷
        datesListInFormat.append(datesList[j].strftime('%Y-%m-%d')) # datetime.date(2020,07,21) -> 2020-07-21로 변환
    latest = max(datesList)

    # pagination
    seedPaginator = Paginator(seeds, 7)
    page = request.GET.get('page')
    posts = seedPaginator.get_page(page)

    context = {
        'seeds':seeds,
        'categories' : categories,
        'categoriesInEng':categoriesInEng,
        'posts':posts,
        'latest' : latest,
    }
    return render(request, 'dansang/seed.html', context)

def seedByCat(request, category):
    seeds = DansangSeed.objects.filter(category_eng=category).order_by('-datePosted')
    categories = SeedCategory.objects.all()
    categoriesInEng = SeedCategoryEng.objects.all()

    # paginate 과정
    seedPaginator = Paginator(seeds, 7)
    page = request.GET.get('page')
    posts = seedPaginator.get_page(page)

    context = {
        'seeds':seeds,
        'categories' : categories,
        'categoriesInEng':categoriesInEng,
        'posts':posts,
        # 'paginator':paginator,
    }
    return render(request, 'dansang/seed.html', context)

def dansangUpdate(request, authuser_id, slug):
    thisDansang = DansangInput.objects.get(slug=slug)

    categoryList = list(DansangInput.objects.filter(authuser=request.user).values_list('category', flat=True).distinct())
    indexList = [*range(1, len(categoryList)+1, 1)] # range 앞에 *을 붙이는 이유는, 저걸 없애면 range()를 알아먹지 못한다.
    # 이제 이걸 [{index: category}, {index: category}, {index: category}, ...]의 꼴로 만들어야 해
    categories = []
    for i in range(0,len(categoryList)):
        catDict = {}
        catDict[indexList[i]] = categoryList[i]
        categories.append(catDict)

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
            # Subtitle이 없다면 First Sentence로 대체하려 했으나...
            # PROBLEM : 본문에서 첫문장이 짧고, 그 다음에 줄바꿈을 하면 그 줄바꿈(tag)이 그대로 subtitle에 반영된다.
            # 즉, subtitle이 없는 경우 contents의 첫 부분을 가져오는데, 문제는 html tag가 모두 포함된다는 것.
            if instance.subtitle == "":
                instance.subtitle = "&nbsp;"

            # 카테고리 영문으로 변경
            catByUser = instance.category
            instance.categoryEng = trans(catByUser)

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

# 각 '씨앗'의 클릭 수를 세는 view입니다. 지금은 중요하지 않아요!
def add_click(request):
    thisId = request.GET.get("seedId", None)
    thisSeed = DansangSeed.objects.get(pk=thisId)
    thisSeed.clicks = F('clicks') + 1
    thisSeed.save()

    return HttpResponse()   # 이건 솔직히 왜 해야하는지 모르겠음. 근데 아무것도 안해주면 it returned None instead라는 에러 뜸.

########## 이건 뭐지...? ##########
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

