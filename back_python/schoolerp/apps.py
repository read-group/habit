from django.apps import AppConfig


class SchoolerpConfig(AppConfig):
    name = 'schoolerp'
    verbose_name = "学校信息"
    def ready(self):
        pass
