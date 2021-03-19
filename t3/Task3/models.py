from django.db import models

# Create your models here.
class Event_brite(models.Model):
    ID = models.AutoField
    Event_Title = models.CharField(max_length=500)
    URL = models.CharField(max_length=500)
    Date_time = models.CharField(max_length=500)
    Category = models.CharField(max_length=500)
    def __str__(self):
    	return self.Event_Title

class Insider(models.Model):
    ID = models.AutoField
    Event_Title = models.CharField(max_length=500)
    URL = models.CharField(max_length=500)
    Date_time = models.CharField(max_length=500)
    Category = models.CharField(max_length=500)
    def __str__(self):
    	return self.Event_Title

