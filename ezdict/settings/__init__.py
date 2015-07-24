from split_settings.tools import optional, include
import os

# Must bypass this block if another settings module was specified.
if os.environ['DJANGO_SETTINGS_MODULE'] == 'ezdict.settings':
    include(
        'components/settings.py',

        'components/db.local.py',
        optional('components/db.prod.py'),

        'components/static.local.py',
        optional('components/static.prod.py'),

        scope=globals()
    )