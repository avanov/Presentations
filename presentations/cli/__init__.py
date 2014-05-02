import codecs
from tempfile import NamedTemporaryFile
from pkg_resources import resource_filename

from plim.console import plimc


def present(args=None, stdout=None):
    template = NamedTemporaryFile(mode='w', encoding='utf-8')
    with codecs.open('django-adt.slides', mode='r', encoding='utf-8') as presentation_file:
        base_path = resource_filename('presentations', 'templates/base.plim')
        with codecs.open(base_path, mode='r', encoding='utf-8') as base_file:
            base_template = base_file.read()
            presentation_template = presentation_file.read()
            base_template = base_template.replace('{{{ presentation_slides }}}', presentation_template)
            template.write(base_template)
            template.flush()
    args = [
        '--encoding', 'utf8',
        '--preprocessor', 'presentations:preprocessor',
        '-o', 'django-adt.html',
        '--html',
        template.name
    ]
    return plimc(args, stdout)
