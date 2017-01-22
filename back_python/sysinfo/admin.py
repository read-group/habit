from django.contrib import admin

# Register your models here.
from sysinfo.models import Honor
from sysinfo.models import Params


admin.site.register(Honor)
admin.site.register(Params)
