from plim.console import plimc


def present(args=None, stdout=None):
    args = [
        '--encoding', 'utf8',
        '--preprocessor', 'presentations:preprocessor',
        #'--html',
        'example.slides'
    ]
    return plimc(args, stdout)
