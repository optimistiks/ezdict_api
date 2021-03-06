from split_settings.tools import optional, include
import os

# Must bypass this block if another settings module was specified.
if os.environ['DJANGO_SETTINGS_MODULE'] == 'ezdict.settings':
    include(
        'components/settings.py',
        optional('components/settings.local.py'),
        optional('components/ezdict.local.py'),
        optional('components/db.local.py'),
        optional('components/static.local.py'),
        scope=globals()
    )
