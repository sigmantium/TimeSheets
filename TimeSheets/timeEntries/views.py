from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic.dates import WeekArchiveView
from datetime import date
from django.views.generic.base import RedirectView

from .models import TimeEntry

# Create your views here.

class TimeEntriesWeekView(WeekArchiveView):
    queryset = TimeEntry.objects.all()
    date_field = "start_time"
    week_format = "%W"
    allow_future = False
    allow_empty = True

class TimeEntriesRedirectView(RedirectView):

    permanent = True
    query_string = True
    pattern_name = 'timeEntries:view-specific-week'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['week'] = date.today().isocalendar()[1]
        kwargs['year'] = date.today().year
        return super().get_redirect_url(*args, **kwargs)

def new(request):
    return render(request, 'timeEntries/new.html')

def view(request, entry_id):
    try:
        entry = TimeEntry.objects.get(pk=entry_id)
    except TimeEntry.DoesNotExist:
        raise Http404("Time Entry does not exist")
    return render( request, 'timeEntries/view.html', {'entry':entry})