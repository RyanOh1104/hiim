from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import 
from .models import 
from django.utils import timezone
from datetime import datetime, date
from django_slugify_processor.text import slugify
# Create your views here.

@login_required
def qandainput(request):
    pass

@login_required
def qandamain(request):
    pass