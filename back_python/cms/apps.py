from django.apps import AppConfig


class CmsConfig(AppConfig):
    name = 'cms'
    verbose_name = "内容管理"
    od=8
    def ready(self):
        pass
