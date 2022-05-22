# read version from installed package
from importlib_metadata import version
#from os.path import dirname, basename, isfile, join

from pkgutil import ImpImporter
from .Listener import *
from .MultiListener import *
# from .SingleListener import *


__version__ = version("mkply")
#modules = glob.glob(join(dirname(__file__), "*.py"))
#__all__ = ["Listener", "MultiListener", "SingleListener"]#[ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]