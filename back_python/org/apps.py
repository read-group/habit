from django.apps import AppConfig


class OrgConfig(AppConfig):
    name = 'org'
    verbose_name = "4:家庭信息"
    def ready(self):
        pass
