from django.apps import AppConfig


class OrgConfig(AppConfig):
    name = 'org'
    verbose_name = "家庭信息"
    od=4
    def ready(self):
        pass
