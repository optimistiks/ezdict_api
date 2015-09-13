from django.apps import AppConfig


class TranslationHistoryConfig(AppConfig):

    name = 'ezdict.translation_history'
    verbose_name = 'Translation History'

    def ready(self):
        # import signal handlers
        import ezdict.translation_history.handlers
