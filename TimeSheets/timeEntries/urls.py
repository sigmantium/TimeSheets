from django.urls import path
from timeEntries.views import TimeEntriesWeekView
from datetime import datetime
from time import strftime

from . import views

app_name = 'timeEntries'

urlpatterns = [
     path('', views.listredirect, name="view-current-week"),
     path('<int:year>/<int:week>/',
          TimeEntriesWeekView.as_view(),
          name="view-specific-week"),
    path('<int:entry_id>', views.view, name='view'),
    path('<int:entry_id>/edit', views.view, name='view'),
    path('new', views.new, name='new'),
]