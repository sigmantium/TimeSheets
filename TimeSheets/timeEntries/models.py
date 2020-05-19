from django.db import models
from clients.models import Client
from django.contrib.auth.models import User

# Create your models here.

class EntryCode(models.Model):
    code_id = models.IntegerField()
    description = models.CharField(max_length=50)

    def __str__(self):
        return  "["+ str(self.code_id) + "] "+ self.description

class TimeEntry(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    billable = models.BooleanField(default=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    code = models.ForeignKey(EntryCode, on_delete=models.DO_NOTHING, null=True, blank=True)

    def open(self):
        if not self.end_time:
            return True

    def logged_time(self):
        if self.end_time:
            return self.end_time - self.start_time
        else:
            return "TBD"
        
    def __str__(self):
        return str(self.pk)