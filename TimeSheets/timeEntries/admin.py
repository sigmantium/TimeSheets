from django.contrib import admin

from .models import EntryCode,TimeEntry
# Register your models here.


admin.site.register(EntryCode)
admin.site.register(TimeEntry)