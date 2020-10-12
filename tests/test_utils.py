from flask_vue_sfc.utils import VueComponent, VueChildComponent, SFC


def test_render_html():
    template = VueComponent('<div class="example">[[message]]</div>', '', lambda: 1)
    template.app_id = '1'
    assert template.render_html() == '<div id=1 ><div class=example >[[message]]</div></div>'


def test_render_child_html():
    template = VueChildComponent('Test', '<div class="example">[[message]]</div>', '', lambda: 1)
    template.app_id = '1'
    assert template.render_html() == '<script type="text/x-template" id=1-template ><div id=1 ><div class=example >[[message]]</div></div></script>'


def test_render_vue_component__no_child():
    script = '''
    export default {
      name: 'Test',
      data() {
        return {
          message: 'test'
        }
      }
    }
    '''
    component = VueComponent('<div class="example">[[message]]</div>', script, lambda: '1')
    sfc = component.render()
    assert isinstance(sfc, SFC)
    assert sfc.script == "new Vue({el:'#1',delimiters:['[[',']]'],name:'Test',data(){return{message:'test'}}})"
    assert sfc.html == '<div id=1 ><div class=example >[[message]]</div></div>'
    assert sfc.children is None


def test_render_vue_child_component__no_child():
    script = '''
    export default {
      name: 'Test',
      data() {
        return {
          message: 'test'
        }
      }
    }
    '''
    component = VueChildComponent('Test', '<div class="example">[[message]]</div>', script, lambda: '1')
    sfc = component.render()
    assert isinstance(sfc, SFC)
    assert sfc.script == "Vue.component('Test',{template:'#1-template',delimiters:['[[',']]'],name:'Test',data(){return{message:'test'}}})"
    assert sfc.html == '<script type="text/x-template" id=1-template ><div id=1 ><div class=example >[[message]]</div></div></script>'
    assert sfc.children is None


def test_render_vue_component__with_child():
    script = '''
    import Test2 from './Test2'
    
    export default {
      name: 'Test',
      components: {
        Test2
      },
      data() {
        return {
          message: 'test'
        }
      }
    }
    '''
    child_html = '<div class="child">[[message]]</div>'
    child_script = '''
    export default {
      name: 'Test2',
      data() {
        return {
          message: 'test2'
        }
      }
    }
    '''

    def child_component_loader(template_name):
        return child_html, child_script

    component = VueComponent('<div class="example">[[message]]</div>', script, lambda: '1', child_component_loader)
    sfc = component.render()
    assert sfc.children is not None
    assert isinstance(sfc.children[0], SFC)
    assert sfc.children[
               0].script == "Vue.component('Test2',{template:'#1-template',delimiters:['[[',']]'],name:'Test2',data(){return{message:'test2'}}})"
    assert sfc.children[
               0].html == '<script type="text/x-template" id=1-template ><div id=1 ><div class=child >[[message]]</div></div></script>'


def test_render_vue_child_component__with_child():
    script = '''
    import Test2 from './Test2'

    export default {
      name: 'Test',
      components: {
        Test2
      },
      data() {
        return {
          message: 'test'
        }
      }
    }
    '''
    child_html = '<div class="child">[[message]]</div>'
    child_script = '''
    export default {
      name: 'Test2',
      data() {
        return {
          message: 'test2'
        }
      }
    }
    '''

    def child_component_loader(template_name):
        return child_html, child_script

    component = VueChildComponent('Test', '<div class="example">[[message]]</div>', script, lambda: '1',
                                  child_component_loader)
    sfc = component.render()
    assert sfc.children is not None
    assert isinstance(sfc.children[0], SFC)
    assert sfc.children[
               0].script == "Vue.component('Test2',{template:'#1-template',delimiters:['[[',']]'],name:'Test2',data(){return{message:'test2'}}})"
    assert sfc.children[
               0].html == '<script type="text/x-template" id=1-template ><div id=1 ><div class=child >[[message]]</div></div></script>'


def test_render_sfc__no_child():
    script = "new Vue({el:'#1',name:'Test',data(){return{message:'test'}}})"
    html = '<div id=1 ><div class=example >[[message]]</div></div>'
    sfc = SFC(html, script)
    expected = (
        "\n"
        "<div id=1 ><div class=example >[[message]]</div></div>\n"
        "<script>\n"
        "new Vue({el:'#1',name:'Test',data(){return{message:'test'}}})\n"
        "</script>\n"
    )
    assert str(sfc) == expected


def test_render_sfc__with_child():
    script = "new Vue({el:'#1',name:'Test',data(){return{message:'test'}}})"
    html = '<div id=1 ><div class=example >[[message]]</div></div>'
    child_script = "Vue.component('Test',{template:'#1-template',name:'Test',data(){return{message:'test'}}})"
    child_html = '<script type="text/x-template" id=1-template ><div id=1 ><div class=example >[[message]]</div></div></script>'
    child_sfc = SFC(child_html, child_script)
    sfc = SFC(html, script, children=[child_sfc])
    expected = (
        "\n"
        '<script type="text/x-template" id=1-template ><div id=1 ><div class=example >[[message]]</div></div></script>\n'
        '<div id=1 ><div class=example >[[message]]</div></div>\n'
        '<script>\n'
        "Vue.component('Test',{template:'#1-template',name:'Test',data(){return{message:'test'}}})\n"
        "new Vue({el:'#1',name:'Test',data(){return{message:'test'}}})\n"
        '</script>\n'
    )
    assert str(sfc) == expected
