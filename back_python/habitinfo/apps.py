from django.apps import AppConfig


class HabitinfoConfig(AppConfig):
    name = 'habitinfo'
    verbose_name = "习惯信息"
    od=2
    def ready(self):
        pass
