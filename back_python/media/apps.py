from django.apps import AppConfig


class MediaConfig(AppConfig):
    name = 'media'
    verbose_name = "媒体文件"
    od=7
    def ready(self):
        pass
