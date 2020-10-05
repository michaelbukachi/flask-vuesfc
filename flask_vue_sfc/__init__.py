import os

from flask import g, Blueprint, current_app, url_for
from markupsafe import Markup
from py_mini_racer import py_mini_racer

from flask_vue_sfc.helpers import _get_file_contents, VueLoader

VERSION_VUE = '2.6.12'
STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


class VueSFC:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['vue_ssr'] = self

        blueprint = Blueprint('vue_ssr', __name__, template_folder='templates',
                              static_folder='static', static_url_path='/vue_ssr' + app.static_url_path)
        app.register_blueprint(blueprint)

        app.jinja_env.globals['vue_ssr'] = self

        app.config.setdefault('VUE_SERVE_LOCAL', False)
        app.config.setdefault('VUE_USE_MINIFIED', True)

        app.jinja_loader = VueLoader(os.path.join(app.root_path, app.template_folder))

        @app.before_request
        def before_request_func():
            if 'v8' not in g:
                g.v8 = py_mini_racer.MiniRacer()

            vue_tc_filepath = os.path.join(STATIC_DIR, 'js', 'vue-template-compiler.js')
            g.v8.eval(_get_file_contents(vue_tc_filepath))

        @app.teardown_appcontext
        def teardown_v8_engine(exc):
            g.pop('v8', None)

    @staticmethod
    def load_js(version=VERSION_VUE):
        serve_local = current_app.config['VUE_SERVE_LOCAL']

        if current_app.config['VUE_USE_MINIFIED']:
            js_filename = 'js/vue.min.js'
        else:
            js_filename = 'js/vue.js'

        if serve_local:
            js = '<script src="%s"></script>' % url_for('vue_ssr.static', filename=js_filename)
        else:
            js = f'<script src="https://cdn.jsdelivr.net/npm/vue@{version}"></script>'

        return Markup(f'{js}')
