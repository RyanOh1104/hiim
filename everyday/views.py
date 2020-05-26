from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .utils import events_to_json, calendar_options
from .forms import EEverydayInputForm
from .models import EverydayInput, NewEvent
from main.models import UserInfo
from datetime import date
from django.utils import timezone
from django_slugify_processor.text import slugify
import json

# Create your views here.
@login_required
def everydayinput(request):
    today = date.today()
    # setting initial user as current logged in user
    # form = EverydayInputForm(initial={'authuser':request.user})
    form = EEverydayInputForm(initial={'authuser':request.user})

    if request.method == 'POST':
        # form = EverydayInputForm(request.POST)
        form = EEverydayInputForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.authuser = request.user
            # instance.when = today
            # instance.kw1 = str(instance.kw1) + "<br>"
            # instance.kw2 = str(instance.kw2) + "<br>"
            instance.when = str(instance.when)
            instance.end = instance.when
            # instance.slug = 
            # instance.url = 
            instance.save()
            return redirect('/everyday/everydaymain')

    return render(request,'everyday/everydayinput.html', {'form':form, 'today' : today})

def everydaymain(request):
    all_events = NewEvent.objects.all()
    thisUser = UserInfo.objects.get(authuser=request.user)
    if request.GET:  
        event_arr = []
        all_events = NewEvent.objects.all()
        
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.what
            event_sub_arr['start'] = i.when
            event_sub_arr['end'] = i.when
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    context = {
        "events":all_events,
        'thisUser':thisUser
    }
    return render(request,'everyday/everydaymain.html', context)

def all_events(request):
    events = NewEvent.objects.all()
    return HttpResponse(events_to_json(events), content_type='application/json; charset=utf-8')

def everydaydetail(request, authuser_id, slug):
    pass


# 아래 왜 주석처리 되어있는데 코드 변경하면 반영되지?
OPTIONS = """{  timeFormat: "H:mm",
                header: {
                    left: 'prev,next',
                    center: 'title',
                    right: 'Nothing comes here',
                },
                allDaySlot: false,
                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 8,
                maxTime: 20,
                editable: true,
            }"""

# header > center 아래에 원래 'right'도 있었음
# right: 'month, agendaWeek, agendaDay'

# dayClick: function(date, allDay, jsEvent, view) {
#                     if (allDay) {       
#                         $('#calendar').fullCalendar('gotoDate', date)      
#                         $('#calendar').fullCalendar('changeView', 'agendaDay')
#                     }
#                 },
#                 eventClick: function(event, jsEvent, view) {
#                     if (view.name == 'month') {     
#                         $('#calendar').fullCalendar('gotoDate', event.start)      
#                         $('#calendar').fullCalendar('changeView', 'agendaDay')
#                     }
#                 },