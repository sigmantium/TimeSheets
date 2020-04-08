from django.shortcuts import render
from django.http import Http404
from django.views.generic.dates import WeekArchiveView
from time import strftime

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
        print(context['week'])
        context['week'] = context['week']
        return context

def new(request):
    return render(request, 'timeEntries/new.html')

def view(request, entry_id):
    try:
        entry = TimeEntry.objects.get(pk=entry_id)
    except TimeEntry.DoesNotExist:
        raise Http404("Time Entry does not exist")
    return render( request, 'timeEntries/view.html', {'entry':entry})