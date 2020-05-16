from django.contrib import admin
from .models import sites
from .models import indexing,uncrawled,search_text, feedback


admin.site.register(sites)
admin.site.register(indexing)
admin.site.register(uncrawled)
admin.site.register(search_text)
admin.site.register(feedback)
# Register your models here.
