import glob
import os

from flask import g, Blueprint, current_app, url_for
from markupsafe import Markup
from py_mini_racer import py_mini_racer

from flask_vue_sfc.utils import VueLoader, _get_file_contents

VERSION_VUE = '2.6.12'
STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


class VueSFC:

    def __init__(self, app=None, cache=None):
        self.cache = cache
        if app is not None:
            self.init_app(app)

    def init_app(self, app, cache=None):
        if cache is not None:
            self.cache = cache

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['vue_sfc'] = self

        blueprint = Blueprint('vue_sfc', __name__, template_folder='templates',
                              static_folder='static', static_url_path='/vue_sfc' + app.static_url_path)
        app.register_blueprint(blueprint)

        app.jinja_env.globals['vue_sfc'] = self

        app.config.setdefault('VUE_SERVE_LOCAL', False)
        app.config.setdefault('VUE_USE_MINIFIED', True)

        templates_folder = os.path.join(app.root_path, app.template_folder)

        app.jinja_loader = VueLoader(templates_folder)

        @app.before_request
        def before_request_func():
            if self.cache and 'sfc_cache' not in g:
                g.sfc_cache = self.cache

            if 'v8' not in g:
                g.v8 = py_mini_racer.MiniRacer()

            vue_tc_filepath = os.path.join(STATIC_DIR, 'js', 'vue-template-compiler.js')
            g.v8.eval(_get_file_contents(vue_tc_filepath))
            escodegen_filepath = os.path.join(STATIC_DIR, 'js', 'escodegen.js')
            g.v8.eval(_get_file_contents(escodegen_filepath))

        @app.teardown_appcontext
        def teardown(exc):
            if 'sfc_cache' in g:
                g.pop('sfc_cache')

            if 'v8' in g:
                g.pop('v8')

        if app.config.setdefault('VUE_PROD_MODE', False):
            if self.cache is None:
                raise RuntimeError('A cache strategy is required if "VUE_PROD_MODE" is True')

            from flask_vue_sfc.helpers import render_vue_component
            # Get all vue components in templates folder and pre-render them
            with app.app_context():
                g.v8 = py_mini_racer.MiniRacer()
                vue_tc_filepath = os.path.join(STATIC_DIR, 'js', 'vue-template-compiler.js')
                g.v8.eval(_get_file_contents(vue_tc_filepath))
                escodegen_filepath = os.path.join(STATIC_DIR, 'js', 'escodegen.js')
                g.v8.eval(_get_file_contents(escodegen_filepath))

                for filename in glob.iglob(templates_folder + '**/*.vue', recursive=True):
                    vue_file = filename.replace(templates_folder + '/', '')
                    render_vue_component(vue_file)

    @staticmethod
    def load_js(version=VERSION_VUE):
        serve_local = current_app.config['VUE_SERVE_LOCAL']

        if current_app.config['VUE_USE_MINIFIED']:
            js_filename = 'js/vue.min.js'
        else:
            js_filename = 'js/vue.js'

        if serve_local:
            js = '<script src="%s"></script>' % url_for('vue_sfc.static', filename=js_filename)
        else:
            js = f'<script src="https://cdn.jsdelivr.net/npm/vue@{version}"></script>'

        return Markup(f'{js}')
