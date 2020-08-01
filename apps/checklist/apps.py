from django.apps import AppConfig


class ChecklistConfig(AppConfig):
    name = 'apps.checklist'

    def ready(self):
        import apps.checklist.signals
