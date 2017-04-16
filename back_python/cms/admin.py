from django.contrib import admin

# Register your models here.
from cms.models import WxWelcome
from cms.models import LoopHead
# Register your models here.
class WxWelcomeAdmin(admin.ModelAdmin):
    list_display=('code','name','desc')
    # list_filter=('level',)
    # search_fields=['name']

class LoopHeadAdmin(admin.ModelAdmin):
    list_display=('code','status','usage','name','desc')
    # list_filter=('level',)
    # search_fields=['name']

admin.site.register(WxWelcome,WxWelcomeAdmin)
admin.site.register(LoopHead,LoopHeadAdmin)
