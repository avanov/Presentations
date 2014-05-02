from plim import preprocessor_factory
from .parser import PARSERS


preprocessor = preprocessor_factory(custom_parsers=list(PARSERS), syntax='mako')
