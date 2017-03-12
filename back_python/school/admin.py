from django.contrib import admin

# Register your models here.
from .models import School
from .models import ClassGroup

class ClassInline(admin.TabularInline):
    model = ClassGroup
    extra = 3
class SchoolAdmin(admin.ModelAdmin):
    list_display=('code','name')
    inlines = [ClassInline]




admin.site.register(School,SchoolAdmin)
admin.site.register(ClassGroup)
