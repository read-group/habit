from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = "交易信息"
    od=6
    def ready(self):
        pass
