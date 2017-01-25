from django.contrib import admin
from media.models import MediaResource
# Register your models here.
class MediaAdmin(admin.ModelAdmin):
    pass

admin.site.register(MediaResource,MediaAdmin)
