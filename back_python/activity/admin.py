from django.contrib import admin
from activity.models import Activity
from activity.models import ActivityItem
# Register your models here.
# Register your models here.
class ActivityItemInline(admin.TabularInline):
    model = ActivityItem
    extra = 0
    fields=('cat',)
class ActivityAdmin(admin.ModelAdmin):
    change_form_template = 'activity/change_form.html'
    fields=('code','school','name',('startTime','endTime',),('cat','desc'),'img','uplimit','amount','rtnLazyUnit',('status','isTop',),'memo')
    list_display=('code','name','startTime','endTime','status','days','lazyFund')
    inlines = [ActivityItemInline]
    list_filter=('cat','status')
    search_fields=['name']

admin.site.register(Activity,ActivityAdmin)
