import os

from project.conf.database.database import config_dev, config_prod

DATABASES = {
    "default": config_prod(),
    "dev": config_dev(),
}
