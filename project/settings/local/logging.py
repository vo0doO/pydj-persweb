import curses
import logging
import os
import time

from django.conf import settings

DEBUG = True 					# Показывать или нет сообщения уровня DEBUG
USE_COLORS = True 				# Должны ли цвета использоваться при выводе текста

class ColorStreamHandler(logging.Handler):

	def __init__(self):
		logging.Handler.__init__(self)
		self.use_colors = True

		# Инициализировать среду
		curses.setupterm()

		# Получить атрибут цвета переднего плана для этой среды
		self.fcap = curses.tigetstr('setaf')

		# Получить нормальный атрибут
		self.COLOR_NORMAL = curses.tigetstr('sgr0')

		# Get + Сохранить цветовые последовательности
		self.COLOR_INFO = curses.tparm(self.fcap, curses.COLOR_GREEN)
		self.COLOR_ERROR = curses.tparm(self.fcap, curses.COLOR_RED)
		self.COLOR_WARNING = curses.tparm(self.fcap, curses.COLOR_YELLOW)
		self.COLOR_DEBUG = curses.tparm(self.fcap, curses.COLOR_BLUE)

	def color(self, msg, level):
		if level == "INFO":
			return "%s%s%s" % (self.COLOR_INFO, msg, self.COLOR_NORMAL)
		elif level == "WARNING":
			return "%s%s%s" % (self.COLOR_WARNING, msg, self.COLOR_NORMAL)
		elif level == "ERROR":
			return "%s%s%s" % (self.COLOR_ERROR, msg, self.COLOR_NORMAL)
		elif level == "DEBUG":
			return "%s%s%s" % (self.COLOR_DEBUG, msg, self.COLOR_NORMAL)
		else:
			return msg
	
	def emit(self, record):
		record.msg = record.msg.encode('utf-8', 'ignore')
		msg = self.format(record)

		# Это просто удаляет дату и миллисекунды из asctime
		temp = msg.split(']')
		msg = '[' + temp[0].split(' ')[1].split(',')[0] + ']' + temp[1]

		if self.use_colors:
			msg = self.color(msg, record.levelname)
		print(msg)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'file': {
			'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s]::(P:%(process)d T:%(thread)d)::%(module)s - %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
		},
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs', 'info.log'),
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    }
}
