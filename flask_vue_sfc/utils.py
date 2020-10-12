import os

import esprima
from css_html_js_minify import html_minify
from esprima.nodes import Module, ExportDefaultDeclaration, Property, ImportDeclaration, Identifier, Literal, \
    ExpressionStatement, NewExpression, CallExpression, StaticMemberExpression, ArrayExpression
from py_mini_racer import py_mini_racer
from jinja2 import FileSystemLoader

STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


class VueLoader(FileSystemLoader):

    def get_source(self, environment, template):
        if template and template.lower().endswith('.vue'):
            # We don't want jinja to touch  {{ }}
            contents, filename, uptodate = super(VueLoader, self).get_source(environment, template)
            contents = '{% raw %}\n' + contents.replace('</template>', '</template>\n{% endraw %}')
            return contents, filename, uptodate
        return super(VueLoader, self).get_source(environment, template)


class SFC:

    def __init__(self, html, script, children=None):
        self.html = html
        self.script = script
        self.children = children

    def scripts_to_string(self):
        output = ''
        if self.children:
            for child in self.children:
                output += child.scripts_to_string()
        output += (self.script + '\n')
        return output

    def html_to_string(self):
        output = ''
        if self.children:
            for child in self.children:
                output += child.html_to_string()
        output += (self.html + '\n')
        return output

    def __str__(self):
        return '\n' + self.html_to_string() + '<script>\n' + self.scripts_to_string() + '</script>\n'


class VueScript:

    def __init__(self, script, id_generator, child_component_loader=None):
        self.script = script
        self.id_generator = id_generator
        self.child_component_loader = child_component_loader
        self.parsed: Module = esprima.parseModule(script)
        self.imports = {}
        self.app_id = None

    def _load_imports(self):
        if not self.imports:
            for declaration in self.parsed.body:
                if isinstance(declaration, ImportDeclaration):
                    self.imports[f'{declaration.specifiers[0].local.name}'] = f'{declaration.source.value}'

    def _get_component_body(self):
        for declaration in self.parsed.body:
            if isinstance(declaration, ExportDefaultDeclaration):
                return declaration

        return None

    @staticmethod
    def _get_component_path(src):
        if '.vue' not in src.lower():
            src = src + '.vue'
        else:
            src = src.replace('.Vue', '.vue')  # Handle potential case difference

        src = src.replace('./', '')
        return src

    def _infer_components(self, props):
        components = {}
        prop: Property
        for prop in props:
            if prop.value.name in self.imports:
                path = self._get_component_path(self.imports[prop.value.name])
                components[f'{prop.value.name}'] = path

        return components

    def child_components(self):
        self._load_imports()
        body = self._get_component_body()
        if body:
            prop: Property
            for prop in body.declaration.properties:
                if prop.key.name == 'components':
                    return self._infer_components(prop.value.properties)
        return []

    def get_identifier_property(self):
        return Property(
            kind='init',
            key=Identifier('el'),
            computed=False,
            method=False,
            value=Literal(f'#{self.app_id}', f"'#{self.app_id}'"),
            shorthand=False
        )

    def get_delimiter_property(self):
        return Property(
            kind='init',
            key=Identifier('delimiters'),
            computed=False,
            method=False,
            value=ArrayExpression(
                [
                    Literal('[[', "'[['"),
                    Literal(']]', "']]'"),
                ]
            ),
            shorthand=False
        )

    def get_vue_container(self):
        return ExpressionStatement(
            NewExpression(
                callee=Identifier('Vue'),
                args=[]
            )
        )

    def render_script(self, v8=None):
        if v8 is None:
            v8 = py_mini_racer.MiniRacer()
            escodegen_filepath = os.path.join(STATIC_DIR, 'js', 'escodegen.js')
            v8.eval(_get_file_contents(escodegen_filepath))

        new_body = []

        for declaration in self.parsed.body:
            if isinstance(declaration, ImportDeclaration):  # Skip imports
                continue

            if isinstance(declaration, ExportDefaultDeclaration):
                vue_app = self.get_vue_container().toDict()
                obj = declaration.declaration.toDict()
                prop = self.get_identifier_property()
                delimiter_prop = self.get_delimiter_property()
                new_properties = [prop.toDict(), delimiter_prop.toDict()]
                for prop in obj['properties']:
                    if prop['key']['name'] == 'components':  # Skip components property
                        continue

                    new_properties.append(prop)
                obj['properties'] = new_properties
                vue_app['expression']['arguments'] += [obj]
                new_body.append(vue_app)
            else:
                new_body.append(declaration.toDict())
        new_parsed_obj = {
            'type': 'Program',
            'sourceType': 'module',
            'body': new_body
        }
        format_options = v8.eval('escodegen.FORMAT_MINIFY')
        return v8.call('escodegen.generate', new_parsed_obj, dict(format=format_options))


class ChildVueScript(VueScript):

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def get_vue_container(self):
        return ExpressionStatement(
            CallExpression(
                callee=StaticMemberExpression(Identifier('Vue'), Identifier('component')),
                args=[Literal(f'{self.name}', f"'{self.name}'")]
            )
        )

    def get_identifier_property(self):
        return Property(
            kind='init',
            key=Identifier('template'),
            computed=False,
            method=False,
            value=Literal(f'#{self.app_id}-template', f"'#{self.app_id}-template'"),
            shorthand=False
        )


class VueComponent(VueScript):

    def __init__(self, html, script, id_generator, child_component_loader=None):
        super(VueComponent, self).__init__(script=script, id_generator=id_generator, child_component_loader=child_component_loader)
        self.app_id = id_generator()
        self.html = html

    def render_html(self):
        html = (
            f'<div id="{self.app_id}">'
            f'{self.html}'
            '</div>'
        )
        html = html_minify(html)
        # Handler delimiters replacement to prevent conflicts with jinja
        if '{{' in html:
            html = html.replace('{{', '[[')
            html = html.replace('}}', ']]')
        return html

    def render(self, v8=None):
        components = self.child_components()
        children = None
        if components:
            children = []
            for key, val in components.items():
                child_html, child_script = self.child_component_loader(val)
                child = VueChildComponent(key, child_html, child_script, self.id_generator, self.child_component_loader)
                children.append(child.render(v8))
        html = self.render_html()
        script = self.render_script(v8)
        return SFC(html, script, children)


class VueChildComponent(ChildVueScript):

    def __init__(self, name, html, script, id_generator, child_component_loader=None):
        super(VueChildComponent, self).__init__(name=name, script=script, id_generator=id_generator, child_component_loader=child_component_loader)
        self.app_id = id_generator()
        self.html = html

    def render_html(self):
        html = (
            f'<script type="text/x-template" id="{self.app_id}-template">'
            f'<div id="{self.app_id}">'
            f'{self.html}'
            '</div>'
            '</script>'
        )
        html = html_minify(html)
        # Handler delimiters replacement to prevent conflicts with jinja
        if '{{' in html:
            html = html.replace('{{', '[[')
            html = html.replace('}}', ']]')
        return html

    def render(self, v8=None):
        components = self.child_components()
        children = None
        if components:
            children = []
            for key, val in components.items():
                child_html, child_script = self.child_component_loader(val)
                child = VueChildComponent(key, child_html, child_script, self.id_generator, self.child_component_loader)
                children.append(child.render(v8))
        html = self.render_html()
        script = self.render_script(v8)
        return SFC(html, script, children)


def _get_file_contents(path):
    with open(path, 'r') as fp:
        return fp.read()
