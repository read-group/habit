from django.contrib import admin
from org.models import Org
from org.models import Profile
# Register your models here.
class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0

class OrgAdmin(admin.ModelAdmin):
    inlines=[ProfileInline]

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Org,OrgAdmin)
admin.site.register(Profile,ProfileAdmin)
