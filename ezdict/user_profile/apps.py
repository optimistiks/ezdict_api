from django.apps import AppConfig


class UserProfileConfig(AppConfig):

    name = 'ezdict.user_profile'
    verbose_name = 'User Profile'

    def ready(self):
        # import signal handlers
        import ezdict.user_profile.handlers
