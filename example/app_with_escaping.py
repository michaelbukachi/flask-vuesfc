from flask import Flask, render_template

from flask_vue_sfc import VueSFC
from flask_vue_sfc.helpers import render_vue_component


class Config:
    SECRET_KEY = 'some-very-long-secret'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    VueSFC(app)

    @app.route('/')
    def example1():
        component = render_vue_component('index4.vue', message='This is rendered by flask')
        return render_template('example.html', component=component)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
