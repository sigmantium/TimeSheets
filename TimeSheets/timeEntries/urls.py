from django.urls import path
from timeEntries.views import TimeEntriesWeekView, TimeEntriesRedirectView

from . import views

app_name = 'timeEntries'

urlpatterns = [
     path('',
         TimeEntriesRedirectView.as_view(),
         name="view-current-week"),
     path('<int:year>/<int:week>/',
          TimeEntriesWeekView.as_view(),
          name="view-specific-week"),
    path('<int:entry_id>', views.view, name='view'),
]