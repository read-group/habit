from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = "6:交易信息"
    def ready(self):
        pass
