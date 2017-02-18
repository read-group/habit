from django.contrib import admin

# Register your models here.
from cms.models import WxWelcome
# Register your models here.
class WxWelcomeAdmin(admin.ModelAdmin):
    list_display=('code','name','desc')
    # list_filter=('level',)
    # search_fields=['name']

admin.site.register(WxWelcome,WxWelcomeAdmin)
