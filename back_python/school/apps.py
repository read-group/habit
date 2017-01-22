from django.apps import AppConfig


class SchoolConfig(AppConfig):
    name = 'school'
    verbose_name = "1:学校信息"
    def ready(self):
        pass
