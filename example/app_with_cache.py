from flask import Flask, render_template

from flask_vue_sfc import VueSFC
from flask_vue_sfc.helpers import render_vue_component, render_vue_page


class Cache(object):
    def __init__(self):
        self._data = {}

    def get(self, k):
        return self._data.get(k)

    def set(self, k, v, timeout=None):
        self._data[k] = v

    def delete(self, k):
        if k in self._data:
            del self._data[k]


class Config:
    SECRET_KEY = 'some-very-long-secret'
    VUE_PROD_MODE = True


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    VueSFC(app, Cache())

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/example1')
    def example1():
        component = render_vue_component('index1.vue')
        return render_template('example.html', component=component)

    @app.route('/example2')
    def example2():
        component = render_vue_component('index2.vue')
        return render_template('example.html', component=component)

    @app.route('/example3')
    def example3():
        component = render_vue_component('index3.vue')
        return render_template('example.html', component=component)

    @app.route('/example4')
    def example4():
        return render_vue_page('index1.vue')

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
