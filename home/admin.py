from django.contrib import admin
from .models import feedback, uncrawled




class UncrawledAdmin(admin.ModelAdmin):
    search_fields = ['url']

# admin.site.register(indexing)
admin.site.register(uncrawled, UncrawledAdmin)
# admin.site.register(search_text)
admin.site.register(feedback)
# admin.site.register(Index)
# Register your models here.
