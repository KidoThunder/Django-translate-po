import django

__title__ = 'Django Translator-PO'
__version__ = '0.1.0'
__author__ = 'Kido Zhao'
__license__ = 'MIT'
__copyright__ = 'Copyright 2011-2019 Encode OSS Ltd'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

if django.VERSION < (3, 2):
    default_app_config = 'translate_po.apps.TranslatePoConfig'
