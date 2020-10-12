import re
import secrets

from flask import render_template
from flask.globals import _app_ctx_stack
from tinycss2 import parse_stylesheet

from flask_vue_sfc.utils import VueComponent


def _create_random_id():
    return 'vue-sfc-' + secrets.token_hex(6)


def _parse_stylesheet(app_id, css):
    rules = parse_stylesheet(css, True, True)
    final_css = '<style>\n'
    for rule in rules:
        final_css += (f'#{app_id} ' + rule.serialize() + '\n')
    final_css += '</style>'
    return final_css


def _get_template_name_from_import(import_str):
    matches = re.findall(r"^.*['\"](.*)['\"]", import_str)
    if matches:
        return matches[0]
    return None


def _get_template_as_html_and_script(template_name):
    ctx = _app_ctx_stack.top
    t = ctx.app.jinja_env.get_or_select_template(template_name)
    vue = t.render()
    parsed = ctx.g.v8.call('VueTemplateCompiler.parseComponent', vue)
    html = parsed['template']['content']
    script = parsed['script']['content']

    return html, script


def _get_component_name(import_str):
    matches = re.findall(r'import\s*(\w+)\s*.*', import_str)
    return matches[0]


def _render_component(template_name):
    ctx = _app_ctx_stack.top
    html, script = _get_template_as_html_and_script(template_name)
    component = VueComponent(html, script, _create_random_id, _get_template_as_html_and_script)
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
