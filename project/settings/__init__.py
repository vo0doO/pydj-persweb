from split_settings.tools import include, optional

include(
    # Параметры среды загрузки
    'base/env.py',

    optional('local/env.py'), # Подбираем нужные настройки из локальных настроек

    # Тут организуем порядок загрузки из за зависимостей
    'base/secutiry.py',
    'base/paths.py',
    'base/apps.py',
    'base/middleware.py',
    'base/debug_toolbar.py',

    # Загрузить все другие параметры
    'base/*.py',

    optional('local/*.py'), # И остальные параметры из локальный настроек
)
