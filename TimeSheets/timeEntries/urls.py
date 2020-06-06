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
    path('new', views.new, name='new'),
    path('quickCreate', views.quickCreate, name="quick-create"),
    path('quickFinish/<int:entry_id>', views.quickFinish, name="quick-finish"),
    path('edit/<int:entry_id>', views.edit, name="edit")
]