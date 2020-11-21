from djongo import models
from django.utils import timezone


class Site(models.Model):
    url = models.TextField()

    class Meta:
        abstract = True


class SiteRank(models.Model):
    _id = models.ObjectIdField()
    site = models.CharField(max_length=255)
    rank = models.FloatField(default=1.0)
    objects = models.DjongoManager()


class SiteDetail(models.Model):
    _id=models.ObjectIdField()
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, default='')
    desc = models.CharField(max_length=400, default='')
    display = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    words_links = models.CharField(max_length=255, default='-')
    icon = models.CharField(max_length=255, default="/favicon.ico")
    objects=models.DjongoManager()


class RankHandler(models.Model):
    _id = models.ObjectIdField()
    site = models.CharField(max_length=255)
    links = models.ArrayReferenceField(to=SiteDetail, on_delete=models.CASCADE)
    objects = models.DjongoManager()


class uncrawled(models.Model):
    _id = models.ObjectIdField()
    url = models.CharField(max_length=255)
    objects = models.DjongoManager()

    def __str__(self):
        return self.url


'''class Key(models.Model):
    value = models.CharField(max_length=255)''' #ch001


class Key(models.Model):
    value = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Original(models.Model):
    original = models.CharField(max_length=255)
    order = models.IntegerField(max_length=255)
    ktype = models.CharField(max_length=50)

    class Meta:
        abstract = True


class KeyExtract(models.Model):
    _id = models.ObjectIdField()
    key = models.EmbeddedField(model_container=Key)
    file = models.ArrayReferenceField(to=SiteDetail,on_delete=models.CASCADE)
    # priority = models.IntegerField()
    original = models.ArrayField(model_container=Original, null=True)
    objects = models.DjongoManager()


class Index(models.Model):
    # key = models.ArrayReferenceField(to=Key,on_delete=models.CASCADE,null=True) #ch01
    _id = models.ObjectIdField()
    key = models.EmbeddedField(model_container=Key)
    sites = models.ArrayReferenceField(to=SiteDetail, null=True, on_delete=models.CASCADE)
    objects = models.DjongoManager()


class feedback(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    desc = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    object = models.DjongoManager()

    def __str__(self):
        return self.name + " : " + self.email

    def least_desc(self):
        if len(self.desc) <= 20:
            return self.desc
        else:
            return f'{self.desc[:20]}...'

class SearchText(models.Model):
    _id = models.ObjectIdField()
    search_text = models.CharField(max_length=255)
    visit_couont = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0)
    objects = models.DjongoManager()

    def __str__(self):
        return self.search_text
