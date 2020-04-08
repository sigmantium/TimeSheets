from django.urls import path
from timeEntries.views import TimeEntriesWeekView
from time import strftime

from . import views

app_name = 'timeEntries'

urlpatterns = [
     path('',
         TimeEntriesWeekView.as_view(year=strftime('%Y'),week=strftime('%W')),
         name="view-current-week"),
     path('<int:year>/<int:week>/',
          TimeEntriesWeekView.as_view(),
          name="view-specific-week"),
    path('<int:entry_id>', views.view, name='view'),
]