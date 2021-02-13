import secrets

from flask import render_template
from flask.globals import _app_ctx_stack

from flask_vue_sfc.utils import VueComponent


def _create_random_id():
    return 'vue-sfc-' + secrets.token_hex(6)


def _load_template(template_name, **context):
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    t = ctx.app.jinja_env.get_or_select_template(template_name)
    vue = t.render(context)
    parsed = ctx.g.v8.call('VueTemplateCompiler.parseComponent', vue)

    component = {
        'html': parsed['template']['content'],
        'script': parsed['script']['content'],
        'styles': [style['content'] for style in parsed['styles']]
    }

    return component


def _render_component(template_name, **context):
    ctx = _app_ctx_stack.top

    src = _load_template(template_name, **context)
    component = VueComponent(src, _create_random_id, _load_template, context)
    sfc = component.render(ctx.g.v8)
    sfc = str(sfc)
    return sfc


def get_compiled_name(name):
    return name.replace('.vue', '.sfc.html')


def render_vue_component(template_name, **context):
    ctx = _app_ctx_stack.top
    if 'building' not in ctx.g and ctx.app.config['VUE_PROD_MODE']:
        return render_template(get_compiled_name(template_name), **context)

    is_page = context.get('is_page', False)
    component = _render_component(template_name, **context)
    if is_page:
        return render_template('page.html', component=component)
    return component


def render_vue_page(template_name, **context):
    context['is_page'] = True
    return render_vue_component(template_name, **context)
