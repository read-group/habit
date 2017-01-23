from django.contrib import admin
from .models import HabitCatalog
from .models import Habit
# Register your models here.
class HabitInline(admin.TabularInline):
    model = Habit
    extra = 3
class HabitCatalogAdmin(admin.ModelAdmin):
    list_display=('code','name')
    inlines = [HabitInline]

class HabitAdmin(admin.ModelAdmin):
    list_display=('code','name','level')
    list_filter=('level',)
    search_fields=['name']

admin.site.register(HabitCatalog,HabitCatalogAdmin)
admin.site.register(Habit,HabitAdmin)
