from django.urls import path
from timeEntries.views import ArticleWeekArchiveView

from . import views

app_name = 'timeEntries'

urlpatterns = [
     path('',
         ArticleWeekArchiveView.as_view(),
         name="view-current-week"),
    path('<int:entry_id>', views.view, name='view'),
]