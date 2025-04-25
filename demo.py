import gettext
import os
from config.language import set_language

_=set_language('zh_CN')
print(_('hello,you are so beautify'))
