from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    name = 'feedback'
    verbose_name = "打卡信息"
    od=5
    def ready(self):
        pass
