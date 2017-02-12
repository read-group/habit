from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = 'activity'
    verbose_name = "活动信息"
    od=3
    def ready(self):
        pass
