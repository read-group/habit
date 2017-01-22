from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = 'activity'
    verbose_name = "3:活动信息"
    def ready(self):
        pass
