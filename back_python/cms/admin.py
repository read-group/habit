from django.contrib import admin

# Register your models here.
from cms.models import WxWelcome
# Register your models here.
class WxWelcomeAdmin(admin.ModelAdmin):
    pass

admin.site.register(WxWelcome,WxWelcomeAdmin)
