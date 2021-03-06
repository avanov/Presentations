import argparse
import json
import sys
from pathlib import Path
from typing import Mapping
from shutil import rmtree
from itertools import islice


import codecs
from tempfile import NamedTemporaryFile
from pkg_resources import resource_filename

from plim.console import plimc


def is_empty_dir(p: Path) -> bool:
    return p.is_dir() and not bool(list(islice(p.iterdir(), 1)))


def setup(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    sub = subparsers.add_parser('gen', help='Generate self-contained HTML slides from slides templates.')
    sub.add_argument('-s', '--source', help="Path to a presentation file. "
                                            "If not specified, then the data will be read from stdin.")
    sub.add_argument('-o', '--output', required=True,
                     help="Output slides file.")
    sub.add_argument('-f', '--force-overwrite', required=False, action='store_true',
                     help="Overwrite existing files and directories if they already exist"
                     )
    sub.set_defaults(run_cmd=main)
    return sub


def main(args: argparse.Namespace, in_channel=sys.stdin, out_channel=sys.stdout) -> None:
    """ $ <cmd-prefix> gen <source> <target>
    """
    template = NamedTemporaryFile(mode='w', encoding='utf-8')
    if args.source is None:
        read_from = in_channel
    else:
        read_from = Path(args.source).open('r')
    with read_from as f:
        slides = f.read()

    base_path = resource_filename('presentations', 'templates/base.plim')
    with codecs.open(base_path, mode='r', encoding='utf-8') as base_file:
        base_template = base_file.read()
        base_template = base_template.replace('{{{ presentation_slides }}}', slides)
        template.write(base_template)
        template.flush()

    args = [
        '--encoding', 'utf8',
        '--preprocessor', 'presentations:preprocessor',
        '-o', args.output,
        '--html',
        template.name
    ]
    return plimc(args, out_channel)
