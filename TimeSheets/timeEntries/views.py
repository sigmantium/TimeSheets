from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.dates import WeekArchiveView
from time import strftime
from datetime import datetime, timedelta
from django.db.models import Sum,F,DurationField

from .models import TimeEntry, Client

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
        year = int(context['week'].strftime('%Y'))
        nextweek = week+1
        lastweek = week-1
        if week == 52 :
            nextweek = 1
        if week == 1 :
            lastweek = 52
        total_hours = TimeEntry.objects.filter(start_time__week=nextweek, end_time__isnull=False)
        total_hours = total_hours.annotate( time_spent = F('end_time')-F('start_time'))
        total_hours = total_hours.aggregate(Sum('time_spent', output_field=DurationField()))
        total_hours = total_hours.get('time_spent__sum', 0.00)
        context.update({
            'thisweek' : week,
            'nextweek' : nextweek,
            'lastweek' : lastweek,
            'totalhours' : total_hours,
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
    if  request.method == 'POST':
        entry.description = request.POST['description']
        entry.start_time = request.POST['start_time']
        end_time = None
        if request.POST.get('end_time', None):
            end_time = request.POST['end_time']
        entry.end_time = end_time
        billable = False
        if request.POST.get('billable', False) == 'on':
            billable = True
        entry.billable = billable
        client_id = request.POST.get('client', None)
        if( client_id ):
            entry.client = Client.objects.get(pk=client_id)
        else:
            entry.client = None
        entry.save()
        return redirect( 'timeEntries:view', entry_id=entry)
    context={
        'entry':entry,
        'clients': Client.objects.all()
    }
    
    return render(request, 'timeEntries/edit.html', context)

def quickFinish(request, entry_id):
    
    entry = TimeEntry.objects.get(pk=entry_id)
    time = datetime.now() 
    time = time - timedelta( minutes = time.minute % 1, seconds = time.second, microseconds = time.microsecond )
    entry.end_time = time
    entry.save()
    return redirect('timeEntries:view-specific-week', week=datetime.now().strftime('%W'), year=datetime.now().strftime('%Y'))