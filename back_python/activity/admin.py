from django.contrib import admin
from activity.models import Activity
from activity.models import ActivityItem
# Register your models here.
# Register your models here.
class ActivityItemInline(admin.TabularInline):
    model = ActivityItem
    extra = 3
class ActivityAdmin(admin.ModelAdmin):
    list_display=('code','name')
    inlines = [ActivityItemInline]

admin.site.register(Activity,ActivityAdmin)
