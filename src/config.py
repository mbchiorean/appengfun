import os

current_dir = os.path.abspath(os.path.dirname(__file__))
template_path = os.path.join(current_dir, 'templates')
config  = {}
config['webapp2_extras.jinja2'] = {
    'template_path': template_path,
    'environment_args': {
        'autoescape': True,
        'extensions': [
            'jinja2.ext.i18n',
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
        ],
    },
}

