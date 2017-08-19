from django.contrib import admin

# Register your models here.
from .models import School
from .models import ClassGroup

class ClassInline(admin.TabularInline):
    model = ClassGroup
    extra = 0
class SchoolAdmin(admin.ModelAdmin):
    list_display=('id','code','name')
    inlines = [ClassInline]


class ClassGroupAdmin(admin.ModelAdmin):
    list_display=('id','code','name',"creator.userName")

admin.site.register(School,SchoolAdmin)
admin.site.register(ClassGroup,ClassGroupAdmin)
