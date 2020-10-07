from flask_vue_sfc.helpers import _parse_stylesheet


def test_parse_stylesheet():
    css = '''
    .example {
        color: red
    }
    '''
    parsed_css = _parse_stylesheet('test', css)
    assert '#test .example' in parsed_css
    assert '<style>' in parsed_css
    assert '</style>' in parsed_css

