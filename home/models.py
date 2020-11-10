from django.db import models
from django.contrib import admin
from django.utils import timezone



class sites(models.Model):
    url = models.TextField()
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=400)
    domain = models.CharField(max_length=20, default='.com')
    display = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0000)
    indexed = models.BooleanField(default=False)
    words_links = models.CharField(max_length= 255, default = '-')
    icon = models.CharField(max_length=255, default = "/favicon.ico")

    def __str__(self):
        return self.title


class uncrawled(models.Model):
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class indexing(models.Model):
    site_id = models.TextField(default = '')
    key = models.CharField(max_length=255)
    site_ids = models.TextField(default = '')

    def __str__(self):
        return self.key

class feedback(models.Model):

    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    desc=models.TextField()
    report_date=models.DateTimeField(default =timezone.now)
    read = models.BooleanField(default = False)

    def __str__(self):
        return self.name + " : "+self.email

    def least_desc(self):
        if len(self.desc)<=20:
            return f'{self.desc}'
        else:
            return f'{self.desc[:20]}...'
            
class search_text(models.Model):
    search_text = models.CharField(max_length=255)
    visit_couont = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0)

    def __str__(self):
        return self.search_text

