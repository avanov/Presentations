import configparser
import re

from plim import lexer
from plim.util import joined

PARSE_CONFIG_RE = re.compile('config\s+(?P<section>.+)', re.IGNORECASE)

PARSE_PRESENTATION = re.compile('presentation', re.IGNORECASE)
PARSE_SLIDE_RE = re.compile('slide', re.IGNORECASE)
PARSE_FRAGMENT_RE = re.compile('fragment', re.IGNORECASE)
PARSE_CODE_RE = re.compile('code', re.IGNORECASE)


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


def parse_presentation(indent_level, current_line, matched, source, syntax):
    matched = syntax.PARSE_DEF_BLOCK_RE.match('-def presentation()')
    return lexer.parse_def_block(indent_level, current_line, matched, source, syntax)


def parse_slide(indent_level, current_line, matched, source, syntax):
    current_line = current_line.replace('slide', 'section')
    processed_tag, tail_indent, tail_line, source = lexer.parse_tag_tree(indent_level, current_line, matched, source, syntax)
    return processed_tag, tail_indent, tail_line, source


def parse_fragment(indent_level, current_line, matched, source, syntax):
    current_line = '.{}'.format(current_line)
    processed_tag, tail_indent, tail_line, source = lexer.parse_tag_tree(indent_level, current_line, matched, source, syntax)
    return processed_tag, tail_indent, tail_line, source


def parse_code(indent_level, current_line, matched, source, syntax):
    _, __, components, tail, source = lexer.extract_tag_line(current_line, source, syntax)
    parsed_data, tail_indent, tail_line, source = lexer.parse_explicit_literal_no_embedded(
        indent_level,
        lexer.LITERAL_CONTENT_PREFIX,
        matched,
        source,
        syntax
    )
    print (components)
    return current_line, tail_indent, tail_line, source


PARSERS = (
    (PARSE_CONFIG_RE, parse_config),
    (PARSE_PRESENTATION, parse_presentation),
    (PARSE_SLIDE_RE, parse_slide),
    (PARSE_FRAGMENT_RE, parse_fragment),
    (PARSE_CODE_RE, parse_code),
)
