import re
import secrets

from css_html_js_minify import html_minify, css_minify
from css_html_js_minify.js_minifier import js_minify_keep_comments
from flask import render_template
from flask.globals import _app_ctx_stack
from jinja2 import FileSystemLoader
from tinycss2 import parse_stylesheet


class VueLoader(FileSystemLoader):

    def get_source(self, environment, template):
        if template and template.lower().endswith('.vue'):
            # We don't want jinja to touch  {{ }}
            contents, filename, uptodate = super(VueLoader, self).get_source(environment, template)
            contents = '{% raw %}\n' + contents.replace('</template>', '</template>\n{% endraw %}')
            return contents, filename, uptodate
        return super(VueLoader, self).get_source(environment, template)


def _get_file_contents(path):
    with open(path, 'r') as fp:
        return fp.read()


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


def _get_component_name(import_str):
    matches = re.findall(r'import\s*(\w+)\s*.*', import_str)
    return matches[0]


def _render_component(template_name, is_child=False, child_component_name=None):
    ctx = _app_ctx_stack.top
    t = ctx.app.jinja_env.get_or_select_template(template_name)
    vue = t.render()
    app_id = _create_random_id()
    component = ''

    parsed = ctx.g.v8.call('VueTemplateCompiler.parseComponent', vue)
    if is_child:
        template = f'<script type="text/x-template" id="{app_id}-template"><div id="{app_id}">{parsed["template"]["content"]}</div></script>'
    else:
        template = f'<div id="{app_id}">{parsed["template"]["content"]}</div>'
    delimiter_replaced = False
    prefix = None

    # Replace {{ }} with [[ ]] so that vue js syntax is not touched by jinja
    if '{{' in template:
        template = template.replace('{{', '[[')
        template = template.replace('}}', ']]')
        delimiter_replaced = True

    js_script = parsed['script']['content']

    child_imports = re.findall(r'import.*(?:[V|v]ue).*', js_script)
    for imp in child_imports:
        template_name = _get_template_name_from_import(imp)
        if not template_name:
            continue
        component_name = _get_component_name(imp)
        child_component = _render_component(template_name, True, component_name)
        component += (child_component + '\n')
        js_script = js_script.replace(imp, '')

    component += (html_minify(template) + '\n')

    sections = js_script.split('export default')
    if len(sections) == 2:
        first = sections[0].strip()
        if first:
            prefix = first
    js_script = re.findall(r'export default\s*{(.*)}', js_script, re.DOTALL | re.MULTILINE)[0].strip()
    if is_child:
        js_script = f'template: \'#{app_id}-template\',\n' + js_script
    else:
        js_script = f'el: \'#{app_id}\',\n' + js_script

    if delimiter_replaced:
        js_script = 'delimiters: [\'[[\', \']]\'],' + js_script

    if is_child:
        js_script = f'Vue.component(\'{child_component_name}\', {{' + js_script + '})'
    else:
        js_script = 'new Vue({' + js_script + '})'

    js_script = js_minify_keep_comments(js_script)

    # Remove component block
    component_block = re.findall(r'(components.*?)}', js_script)
    if component_block:
        js_script = js_script.replace(component_block[0] + '},', '')

    if prefix:
        js_script = prefix + '\n' + js_script

    js_script = '<script>' + js_script + '</script>'

    component += (js_script + '\n')

    styles = parsed['styles']
    if styles:
        for style in styles:
            component += (css_minify(_parse_stylesheet(app_id, style['content']), noprefix=True) + '\n')
    return component


def render_vue_component(template_name, **context):
    is_page = context.get('is_page', False)
    component = _render_component(template_name)
    print(component)
    if is_page:
        return render_template('page.html', component=component)
    return component


def render_vue_page(template_name):
    return render_vue_component(template_name, is_page=True)
