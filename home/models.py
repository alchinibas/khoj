from djongo import models
from django.utils import timezone


class sites(models.Model):
    url = models.TextField(default='')
    title = models.CharField(max_length=255, default='')
    desc = models.CharField(max_length=400, default='')
    domain = models.CharField(max_length=20, default='.com')
    display = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)

    priority = models.FloatField(default=1.0000)
    indexed = models.BooleanField(default=False)
    words_links = models.CharField(max_length=255, default='')
    icon = models.CharField(max_length=255, default="/favicon.ico")


class Site(models.Model):
    url = models.TextField()

    class Meta:
        abstract = True


class SiteRank(models.Model):
    _id = models.ObjectIdField()
    site = models.EmbeddedField(model_container=Site)
    rank = models.FloatField(default=1.0)
    objects = models.DjongoManager()


class SiteDetail(models.Model):
    _id=models.ObjectIdField()
    site = models.EmbeddedField(model_container=Site)
    title = models.CharField(max_length=255, default='')
    desc = models.CharField(max_length=400, default='')
    domain = models.CharField(max_length=20, default='.com')
    display = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0000)
    indexed = models.BooleanField(default=False)
    words_links = models.CharField(max_length=255, default='-')
    icon = models.CharField(max_length=255, default="/favicon.ico")
    objects=models.DjongoManager()


class RankHandler(models.Model):
    _id = models.ObjectIdField()
    url = models.CharField(max_length=255)
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


class indexing(models.Model):
    key = models.CharField(max_length=255)
    site_id = models.TextField()

    def __str__(self):
        return self.key

class feedback(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    desc = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " : " + self.email

    def least_desc(self):
        if len(self.desc) <= 20:
            return self.desc
        else:
            return f'{self.desc[:20]}...'


class search_text(models.Model):
    search_text = models.CharField(max_length=255)
    visit_couont = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0)

    def __str__(self):
        return self.search_text

class SearchText(models.Model):
    search_text = models.CharField(max_length=255)
    visit_couont = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0)

    def __str__(self):
        return self.search_text


class SearchText(models.Model):
    _id = models.ObjectIdField()
    search_text = models.CharField(max_length=255)
    visit_couont = models.IntegerField(default=0)
    priority = models.FloatField(default=1.0)
    objects = models.DjongoManager()

    def __str__(self):
        return self.search_text
