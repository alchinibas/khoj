from django.contrib import admin
from .models import sites
from .models import indexing,uncrawled,search_text, feedback


class SiteAdmin(admin.ModelAdmin):
    search_fields = ['url']


class UncrawledAdmin(admin.ModelAdmin):
    search_fields = ['url']

admin.site.register(sites, SiteAdmin)
admin.site.register(indexing)
admin.site.register(uncrawled, UncrawledAdmin)
admin.site.register(search_text)
admin.site.register(feedback)
# Register your models here.
