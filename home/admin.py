from django.contrib import admin
from .models import sites
from .models import indexing,uncrawled,reference_directory,search_text


admin.site.register(sites)
admin.site.register(indexing)
admin.site.register(uncrawled)
admin.site.register(reference_directory)
admin.site.register(search_text)
# Register your models here.
