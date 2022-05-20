# read version from installed package
from importlib.metadata import version
from os.path import dirname, basename, isfile, join
import glob
from mkply import Listener
from mkply import MultiListener
from mkply import SingleListener
__version__ = version("mkply")
#modules = glob.glob(join(dirname(__file__), "*.py"))
#__all__ = ["Listener", "MultiListener", "SingleListener"]#[ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]