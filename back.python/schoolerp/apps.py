from django.apps import AppConfig
class SchoolConfig(AppConfig):
    name = 'schoolerp'
    #verbose_name = _("Authentication and Authorization")
    verbose_name = "学校管理"
    def ready(self):
        pass
