from django.contrib import admin
from account.models import Account,SysAccount,SysAccountHistory
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    pass
class SysAccountHistoryInline(admin.TabularInline):
    model = SysAccountHistory
    extra = 3
class SysAccountAdmin(admin.ModelAdmin):
    fields = ('accountType', 'name')
    list_display=('accountType','name','balance')
    inlines = [SysAccountHistoryInline]
admin.site.register(SysAccount,SysAccountAdmin)
admin.site.register(Account,AccountAdmin)
