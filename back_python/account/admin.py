from django.contrib import admin
from account.models import Account,SysAccount,SysAccountHistory
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    pass
class SysAccountHistoryInline(admin.TabularInline):
    model = SysAccountHistory
    extra = 1
class SysAccountAdmin(admin.ModelAdmin):
    fields = ('accountType', 'name','balance')
    readonly_fields=('balance',)
    list_display=('accountType','name','balance')
class SysAccountHistoryAdmin(admin.ModelAdmin):
    fields = ('tradeDate', 'tradeType','tradeAmount')
    list_display=('tradeDate','tradeType','tradeAmount')
    # inlines = [SysAccountHistoryInline]
admin.site.register(SysAccount,SysAccountAdmin)
admin.site.register(Account,AccountAdmin)
