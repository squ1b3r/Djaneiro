import sys

from .commands import *  # noqa

if sys.version_info < (3, 8):
    raise RuntimeError('Some features of Djaneiro require Sublime Text 4 and up.')
