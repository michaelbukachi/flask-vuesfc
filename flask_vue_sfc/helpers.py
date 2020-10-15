import secrets

from flask import render_template
from flask.globals import _app_ctx_stack

from flask_vue_sfc.utils import VueComponent


def _create_random_id():
    return 'vue-sfc-' + secrets.token_hex(6)


def _load_template(template_name):
    ctx = _app_ctx_stack.top
    t = ctx.app.jinja_env.get_or_select_template(template_name)
    vue = t.render()
    parsed = ctx.g.v8.call('VueTemplateCompiler.parseComponent', vue)

    component = {
        'html': parsed['template']['content'],
        'script': parsed['script']['content'],
        'style': [style['content'] for style in parsed['styles']]
    }

    return component


def _render_component(template_name):
    ctx = _app_ctx_stack.top
    src = _load_template(template_name)
    component = VueComponent(src, _create_random_id, _load_template)
    sfc = component.render(ctx.g.v8)

    # styles = parsed['styles']
    # if styles:
    #     for style in styles:
    #         component += (css_minify(_parse_stylesheet(app_id, style['content']), noprefix=True) + '\n')
    return str(sfc)


def render_vue_component(template_name, **context):
    is_page = context.get('is_page', False)
    component = _render_component(template_name)
    if is_page:
        return render_template('page.html', component=component)
    return component


def render_vue_page(template_name):
    return render_vue_component(template_name, is_page=True)
