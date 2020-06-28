import os
import re

from django.conf import settings

UUID4_HEX_REGEX = re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z', re.I)
PATH_TO_LOG = os.path.join(settings.BASE_DIR, 'logs', 'curiosity.log')

PATH_TO_IMG_ORIGINAL = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_ORIGINAL.png"
PATH_TO_IMG_1_COMPOSITE = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_COMPOSITE.png"
PATH_TO_IMG_LOGO_PAINTER = os.path.dirname(os.path.abspath(__file__)) + "/desing/logo-painter.png"
PATH_TO_FONTS = os.path.dirname(os.path.abspath(__file__)) + "/topics/Roboto-Fonts/Roboto-Bold.ttf"
PATH_TO_IMG_BUTTON = os.path.dirname(os.path.abspath(__file__)) + "/Button.png"
PARSER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_DUMP = os.path.join(PARSER_DIR, "apps/curiosity/parser/my_href.db")
URL_DUMP_BACKUP = os.path.dirname(os.path.abspath(__file__)) + "/my_href_backup.db"
PATH_TO_IMG_RESIZE = os.path.dirname(os.path.abspath(__file__)) + "/topics/IMG_RESIZE.png"
