from django.apps import AppConfig


class SchoolConfig(AppConfig):
    name = 'school'
    verbose_name = "学校信息"
    od=1
    def ready(self):
        pass
