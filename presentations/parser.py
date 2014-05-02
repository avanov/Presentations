import configparser
import re

from plim import lexer
from plim.util import joined

PARSE_CONFIG_RE = re.compile('config\s+(?P<section>.+)', re.IGNORECASE)


def parse_config(indent_level, current_line, matched, source, syntax):
    section = matched.group('section')

    parsed_data, tail_indent, tail_line, source = lexer.parse_explicit_literal_no_embedded(
        indent_level,
        lexer.LITERAL_CONTENT_PREFIX,
        matched,
        source,
        syntax
    )
    parsed_data = "[{section}]\n{parsed_data}".format(section=section, parsed_data=parsed_data)
    config = configparser.ConfigParser()
    config.read_string(parsed_data)
    python_config = dict(config.items(section))
    python_config = "CONFIG['{section}'] = {config}".format(section=section, config=python_config)
    buf = ['<%\n', python_config, '\n%>']
    return joined(buf), tail_indent, tail_line, source



PARSERS = (
    (PARSE_CONFIG_RE, parse_config),
)
