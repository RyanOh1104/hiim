from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from main.models import UserInfo
from .forms import AnswerForm
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.utils import timezone
from datetime import datetime, date
from time import strftime
from django.core.paginator import Paginator

###### 중요!!! 유저가 가장 처음에 즉문즉답 기록장을 하면, main페이지가 아닌 첫번째 질문을 던져주자!!!! #####
@login_required
def qandaInput(request): 
    today = date.today()

    # 0. Very first 질문은 query를 하면 empty queryset이 나오므로 별도로 처리
    if not Answer.objects.filter(authuser=request.user):
        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=1)
        formset = AnswerFormSet(queryset=Answer.objects.filter(authuser = request.user, questionNumber=1))
        todaysQuestion = Question.objects.get(number=1)
        if request.method == "POST":
            formset = AnswerFormSet(request.POST)
            if formset.is_valid():
                instance = formset.save(commit=False)
                instance[0].authuser = request.user
                instance[0].questionNumber = 1 # ForeignKey로 하지 않고 이렇게 하는 거 너무 비효율적인가? 나중에 문제가 생기려나?
                instance[0].dateAnswered = str(today)
                instance[0].save()
                return redirect('/qanda/qandamain')

    else: # 처음 질문 이후 모두 해당
        # 가장 최근 질문의 가장 최근 답변일 가져오기!!
        # 1) authuser의 모든 답변들의 questionNumber 가져오기
        latestAnswers = Answer.objects.filter(authuser=request.user).values('questionNumber') # QuerySet
        allNumbers = list(latestAnswers.values('questionNumber')) # 딕셔너리가 들어있는 리스트
        # questionNumber 중 최댓값, 즉 답변을 한 가장 최근 질문의 넘버 가져오기
        numbersList = []
        for i in range(0, len(allNumbers)): # !!!!!! 대체 왜 len()-1이 아닌지 모르겠다!!!!!!
            numbersList.append(*allNumbers[i].values()) # 여기 * operator는 python3 dictionary에 적용된 view?를 없애주는 것.
        latestQuestionNumber = max(numbersList)

        # 2) authuser의, 가장 최근 질문의 가장 최근 dateAnswered값 가져오기
        latestDateAnswered = Answer.objects.filter(authuser=request.user, questionNumber=latestQuestionNumber).values('dateAnswered')
        # allDates의 각 원소는 {'dateAnswered':datetime.date(2020, 07, 21)} 이런 포맷 (python dictionary view)
        allDates = list(latestDateAnswered.values('dateAnswered'))
        # Date 중 최댓값, 즉 가장 최근의 질문의 날짜 가져오기 (바로 위와 정확히 동일)
        datesList = []
        datesListInFormat = []
        for j in range(0, len(allDates)): # !!!!!! 대체 왜 len()-1이 아닌지 모르겠다!!!!!!
            datesList.append(*allDates[j].values()) # 각 원소는 datetime.date(2020,07,21)의 포맷
            datesListInFormat.append(datesList[j].strftime('%Y-%m-%d')) # datetime.date(2020,07,21) -> 2020-07-21로 변환
        latestQuestionDate = max(datesList)

        # 가장 최근 질문의 가장 최근 답변일이 가져와졌다. 이 날짜와 today의 값이 서로 같은지 다른지 확인해줘야 한다.
        AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=1)
        if latestQuestionDate < today:
            # 다음 질문 가져오기 (정상적으로 진행)
            todaysQuestionNumber = latestQuestionNumber + 1
            formset = AnswerFormSet(queryset=Answer.objects.filter(authuser = request.user, questionNumber=todaysQuestionNumber))
            todaysQuestion = Question.objects.get(number=todaysQuestionNumber)
            if request.method == "POST":
                formset = AnswerFormSet(request.POST)
                if formset.is_valid():
                    instance = formset.save(commit=False)
                    instance[0].authuser = request.user
                    instance[0].questionNumber = todaysQuestionNumber # ForeignKey로 하지 않고 이렇게 하는 거 너무 비효율적인가? 나중에 문제가 생기려나?
                    instance[0].dateAnswered = str(today)
                    instance[0].save()
                    '''
                    formset의 경우 instance는 "딕셔너리 in 리스트"의 형태!!
                    가령 이런 식. 맞나?
                    [{authuser:'ryan', questionNumber:1, dateAnswered:'2020-07-20'}]
                    '''

                    # save할 때 문제 생기면 아래 링크 참고 -- iteration해서 for loop으로 저장.
                    # https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#saving-objects-in-the-formset
                    return redirect('/qanda/qandamain')

        elif latestQuestionDate == today: # 즉, 아직 날짜가 지나지 않았을 때
            return redirect('/qanda/qandamain')

    ################### POTENTIAL ERROR ####################
    # 동일한 date에 답변 두개를 입력한다면?
    ########################################################

    thisUser = UserInfo.objects.get(authuser_id=request.user.id)

    context = {
        'formset':formset,
        'todaysQuestion':todaysQuestion,
        'thisUser':thisUser,
    }
    return render(request, 'qanda/qandainput.html', context)

def qandaMain(request):
    thisQuestion = Question.objects.all()
    thisAnswer = Answer.objects.filter(authuser=request.user)
    thisUser = UserInfo.objects.get(authuser_id=request.user.id)

    # 답한 질문만 보이도록 해야 한다.
    # 그러기 위해 input에서 쓴 latestQuestionNumber 변수를 가져오자.
    # 일단, 답변을 한 모든 질문들의 번호
    latestAnswers = Answer.objects.filter(authuser=request.user).values('questionNumber') # QuerySet
    allNumbers = list(latestAnswers.values('questionNumber')) # 딕셔너리가 들어있는 리스트
    # questionNumber 중 최댓값, 즉 답변을 한 가장 최근 질문의 넘버 가져오기
    numbersList = []
    for i in range(0, len(allNumbers)):
        numbersList.append(*allNumbers[i].values()) # 여기 * operator는 python3 dictionary에 적용된 view?를 없애주는 것.
    latestQuestionNumber = max(numbersList)

    # pagination
    qandaPaginator = Paginator(thisQuestion, 7)
    page = request.GET.get('page')
    posts = qandaPaginator.get_page(page)

    context = {
        'thisQuestion':thisQuestion,
        'thisAnswer':thisAnswer,
        'thisUser':thisUser,
        'latestQuestionNumber' : latestQuestionNumber,
        'posts':posts,
    }

    return render(request, 'qanda/qandamain.html', context)

def qandaDetail(request, questionNumber):
    thisQuestion = Question.objects.get(number=questionNumber)
    thisAnswer = Answer.objects.filter(authuser=request.user, questionNumber=questionNumber).order_by('dateAnswered')
    thisUser = UserInfo.objects.get(authuser_id=request.user.id)

    # 아직 답하지 않은 질문의 detail 페이지로 갔을 때(주소창에 직접 입력하여) 막는 기능이 필요하다.
    # 그러기 위해 input에서 쓴 latestQuestionNumber 변수를 가져오자.
    # 일단, 답변을 한 모든 질문들의 번호
    latestAnswers = Answer.objects.filter(authuser=request.user).values('questionNumber') # QuerySet
    allNumbers = list(latestAnswers.values('questionNumber')) # 딕셔너리가 들어있는 리스트
    # questionNumber 중 최댓값, 즉 답변을 한 가장 최근 질문의 넘버 가져오기
    numbersList = []
    for i in range(0, len(allNumbers)):
        numbersList.append(*allNumbers[i].values()) # 여기 * operator는 python3 dictionary에 적용된 view?를 없애주는 것.
    latestQuestionNumber = max(numbersList)
    
    # 이제, argument인 'questionNumber'가 Answer 모델에 존재하는지 보고, 있으면 보여주고 없으면 다른 창으로 redirect.
    # 먼저 있다면,
    if thisAnswer.exists(): 
        context = {
            'thisQuestion':thisQuestion,
            'thisAnswer':thisAnswer,
            'thisUser':thisUser,
        }

        return render(request, 'qanda/qandadetail.html', context)
    else: 
        return redirect('/qanda/qandamain')

def qandaUpdate(request, questionNumber):
    today = date.today()
    thisQuestion = Question.objects.get(number=questionNumber)
    thisAnswer = Answer.objects.filter(authuser=request.user, questionNumber=questionNumber)
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=1)
    formset = AnswerFormSet(queryset=Answer.objects.filter(authuser = request.user, questionNumber=questionNumber))
    thisUser = UserInfo.objects.get(authuser_id=request.user.id)

    # 답변한 질문만 보이도록!!
    latestAnswers = Answer.objects.filter(authuser=request.user).values('questionNumber') # QuerySet
    allNumbers = list(latestAnswers.values('questionNumber')) # 딕셔너리가 들어있는 리스트
    # questionNumber 중 최댓값, 즉 답변을 한 가장 최근 질문의 넘버 가져오기
    numbersList = []
    for i in range(0, len(allNumbers)):
        numbersList.append(*allNumbers[i].values()) # 여기 * operator는 python3 dictionary에 적용된 view?를 없애주는 것.
    latestQuestionNumber = max(numbersList)

    if thisAnswer.exists(): 
        if request.method == "POST":
            formset = AnswerFormSet(request.POST)
            if formset.is_valid():
                instance = formset.save(commit=False)
                instance[0].authuser = request.user
                instance[0].questionNumber = questionNumber # ForeignKey로 하지 않고 이렇게 하는 거 너무 비효율적인가? 나중에 문제가 생기려나?
                # instance[0].dateAnswered = str(today) -- 이게 있으면 수정된 날짜가 저장되어버린다.
                instance[0].save()

                return redirect('/qanda/qandamain')

        context = {
            'thisQuestion' : thisQuestion,
            'formset':formset,
            'thisUser': thisUser,
        }

        return render(request, 'qanda/update.html', context)

    else: 
        return redirect('/qanda/qandamain')

def noMoreForToday(request):
    return render(request, 'qanda/nomorefortoday.html')

