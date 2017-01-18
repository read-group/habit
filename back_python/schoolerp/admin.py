from django.contrib import admin

# Register your models here.
from .models import School
from .models import ClassGroup
admin.site.register(School)
admin.site.register(ClassGroup)
