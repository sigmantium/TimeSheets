from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.dates import WeekArchiveView
from time import strftime
from datetime import datetime

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
    return render(request, 'timeEntries/new.html')

def view(request, entry_id):
    try:
        entry = TimeEntry.objects.get(pk=entry_id)
    except TimeEntry.DoesNotExist:
        raise Http404("Time Entry does not exist")
    return render( request, 'timeEntries/view.html', {'entry':entry})

def listredirect(request):
    return redirect('timeEntries:view-specific-week', week=datetime.now().strftime('%W'), year=datetime.now().strftime('%Y'))