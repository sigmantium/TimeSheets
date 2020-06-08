from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.dates import WeekArchiveView
from time import strftime
from datetime import datetime, timedelta

from .models import TimeEntry

# Create your views here.

class TimeEntriesWeekView(WeekArchiveView):
    queryset = TimeEntry.objects.all()
    date_field = "start_time"
    week_format = "%W"
    allow_future = False
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week = int(context['week'].strftime('%W'))
        nextweek = week+1
        lastweek = week-1
        if week == 52 :
            nextweek = 1
        if week == 1 :
            lastweek = 52

        context.update({
            'thisweek' : week,
            'nextweek' : nextweek,
            'lastweek' : lastweek,
        })
        return context

def new(request):
    entry = TimeEntry.objects.create(
        owner = request.user,
        start_time = datetime.now()
    )
    return redirect('timeEntries:edit', entry_id=entry )

def view(request, entry_id):
    try:
        entry = TimeEntry.objects.get(pk=entry_id)
    except TimeEntry.DoesNotExist:
        raise Http404("Time Entry does not exist")
    return render( request, 'timeEntries/view.html', {'entry':entry})

def listredirect(request):
    return redirect('timeEntries:view-specific-week', week=datetime.now().strftime('%W'), year=datetime.now().strftime('%Y'))

def quickCreate(request):
    
    time = datetime.now() 
    time = time - timedelta( minutes = time.minute % 1, seconds = time.second, microseconds = time.microsecond )
    entry = TimeEntry.objects.create(
        owner = request.user,
        start_time = time
    )
    return redirect('timeEntries:view-specific-week', week=datetime.now().strftime('%W'), year=datetime.now().strftime('%Y'))

def edit(request, entry_id):
    try:
        entry = TimeEntry.objects.get(pk=entry_id)
    except TimeEntry.DoesNotExist:
        raise Http404("Time Entry does not exist")
    return render(request, 'timeEntries/edit.html', {'entry':entry})

def quickFinish(request, entry_id):
    
    entry = TimeEntry.objects.get(pk=entry_id)
    time = datetime.now() 
    time = time - timedelta( minutes = time.minute % 1, seconds = time.second, microseconds = time.microsecond )
    entry.end_time = time
    entry.save()
    return redirect('timeEntries:view-specific-week', week=datetime.now().strftime('%W'), year=datetime.now().strftime('%Y'))