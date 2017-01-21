from django.contrib import admin

# Register your models here.
from .models import School
from .models import ClassGroup
from .models import HabitCatalog
from .models import Habit


class ClassInline(admin.TabularInline):
    model = ClassGroup
    extra = 3
class SchoolAdmin(admin.ModelAdmin):
    list_display=('code','name')
    inlines = [ClassInline]


class HabitInline(admin.TabularInline):
    model = Habit
    extra = 3
class HabitCatalogAdmin(admin.ModelAdmin):
    list_display=('code','name')
    inlines = [HabitInline]

admin.site.register(School,SchoolAdmin)
admin.site.register(ClassGroup)

admin.site.register(HabitCatalog,HabitCatalogAdmin)
admin.site.register(Habit)
