from django.db import models
from datetime import datetime  

# Create your models here.
class MyBook(models.Model):
    acc_id = models.CharField(max_length=20, default='default')
    image = models.CharField(max_length = 255, blank=True, null=True)
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    publisher = models.CharField(max_length = 100)
    pubdate = models.CharField(max_length = 100)
    isbn = models.CharField(max_length = 100)
    start = models.DateField(default=datetime.now, blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    idea = models.TextField(null=True)
    score = models.IntegerField(default = 0, null=True)

    def __str__(self):
        return self.title

class Sentence(models.Model):
    id = models.AutoField(primary_key=True)
    acc_id = models.CharField(max_length=20, default='default')
    isbn = models.CharField(max_length = 100)
    page = models.CharField(max_length = 100, default=0)
    sentence = models.TextField(null=True)
    date = models.DateField(default = datetime.now)

    def __str__(self):
        return self.sentence