from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, inlineformset_factory
from .models import Question, Answer
from django.utils import timezone
from datetime import datetime, date
from django_slugify_processor.text import slugify
# Create your views here.

@login_required
def qandainput(request):
    
    # today = datetime.today() # 'date' field에 들어갈 변수
    pass    

@login_required
def qandamain(request):
    pass