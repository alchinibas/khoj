from djongo import models
from django.contrib import admin
from django.utils import timezone
# from django import forms



class sites(models.Model):
    url = models.TextField(default = '')
    title = models.CharField(max_length=255,default = '')
    desc = models.CharField(max_length=400,default = '')
    domain = models.CharField(max_length=20, default='.com')
    display = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0000)
    indexed = models.BooleanField(default=False)
    words_links = models.CharField(max_length= 255, default = '-')
    icon = models.CharField(max_length=255, default = "/favicon.ico")

    class Meta:
        abstract = True

class uncrawled(models.Model):
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url

class Key(models.Model):
    value = models.CharField(max_length=255)
    class Meta:
        abstract=True

class Original(models.Model):
    original = models.CharField(max_length=255)
    order = models.IntegerField(max_length=255)
    priority = models.IntegerField()

    class Meta:
        abstract=True

class indexing(models.Model):
    key = models.EmbeddedField(model_container = Key,null = True)
    previous_keys = models.ArrayField(model_container = Key,null=True)
    file = models.EmbeddedField(model_container = sites, null = True,)


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

