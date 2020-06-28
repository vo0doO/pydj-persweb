# Построить пути внутри проекта, как это: os.path.join(BASE_DIR, ...)
import os

from django.conf import settings

from project.conf.paths import paths

paths.config()
settings.__setattr__(
                "PROJECT_DIR", 
                os.path.join(settings.BASE_DIR, "project")
            )

settings.__setattr__("APPS_DIR", os.path.join(settings.PROJECT_DIR, "apps/"))
