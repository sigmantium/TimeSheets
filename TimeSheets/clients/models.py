from django.db import models

# Create your models here.

class Client(models.Model):
    
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Contact(models.Model):

    name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 100)
    office_phone = models.IntegerField()
    mobile_number = models.IntegerField()
    company = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

