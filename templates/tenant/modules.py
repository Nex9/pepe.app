import logging

# TODO loop this

try: from imageapp.modules import *
except Exception,e: logging.info('import imageapp modules: %s' % e)

try: from blogapp.modules import *
except Exception,e: logging.info('import blogapp modules: %s' % e)

try: from base.modules import *
except Exception,e: logging.info('import base modules: %s' % e)