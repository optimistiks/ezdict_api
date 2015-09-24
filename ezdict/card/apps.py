from django.apps import AppConfig


class CardConfig(AppConfig):

    name = 'ezdict.card'
    verbose_name = 'Card'

    def ready(self):
        # import signal handlers
        import ezdict.card.handlers
