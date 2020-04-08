from django.shortcuts import render
from django.http import Http404
from django.views.generic.dates import WeekArchiveView
from datetime import date

from .models import TimeEntry

# Create your views here.

class ArticleWeekArchiveView(WeekArchiveView):
    queryset = TimeEntry.objects.all()
    date_field = "start_time"
    week_format = "%W"
    allow_future = False
    allow_empty = True

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      print("got here")
      if 'week' in self.request.GET:
           context['week'] = self.request.GET['week']
           context['year'] = self.request.GET['year']
      else:
            context.update({
            'week': self.request.GET.get('week', date.today().isocalendar()[1]),
            'year': self.request.GET.get('year', date.today().year),
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