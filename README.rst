===============
Flask-VueSFC
===============
.. image:: https://img.shields.io/pypi/v/Flask-VueSFC.svg
    :target: https://pypi.python.org/pypi/Flask-VueSFC/
.. image:: https://img.shields.io/pypi/l/Flask-VueSFC.svg
    :target: https://pypi.python.org/pypi/Flask-VueSFC
.. image:: https://img.shields.io/pypi/pyversions/Flask-VueSFC.svg
    :target: https://pypi.python.org/pypi/Flask-VueSFC/
.. image:: https://img.shields.io/pypi/status/Flask-VueSFC.svg
    :target: https://pypi.python.org/pypi/Flask-VueSFC/

Flask-VueSFC is a Flask extension that translates and renders `Vue.js
<http://vuejs.org>`_ Single File Components.

In short, it translates code like this ::

  <template>
    <div>Current time is: <b>{{ date }}</b></div>
    </template>
  <script>
    Vue.use(vueMoment)

    export default  {
      name: 'App',
      data() {
        return {
          date: null
        }
      },
      created() {
        this.setCurrentTime()
      },
      methods: {
        setCurrentTime() {
          this.date = this.$moment().format('dddd, MMMM Do YYYY, h:mm:ss a')
          setTimeout(() => {
            this.setCurrentTime()
          }, 1000)
        }
      }
    }
  </script>


into this ::

  <div id="vue-sfc-996dcfa8e795">
    <div>Current time is: <b>[[ date ]]</b>
    </div>
  </div>
  <script>
    Vue.use(vueMoment);
    new Vue({
      el:'#vue-sfc-996dcfa8e795',
      delimiters:['[[',']]'],
      name:'App',
      data(){
        return{
          date: null
        }
      },
      created() {
        this.setCurrentTime()
      },
      methods: {
        setCurrentTime() {
          this.date = this.$moment().format('dddd, MMMM Do YYYY, h:mm:ss a');
          setTimeout(()=>{
            this.setCurrentTime()
          },1e3)
        }
      }
    })
  </script>

which renders something like this:

Current time is: **Friday, October 16th 2020, 2:35:27 am**

**Disclaimer:**
    This project is not a replacement for ``webpack`` in any way. Depending on the complexity of one's project and specific cases, this project might
    or might not be useful.

    Any third party JS library used must be UMD compatible.

    All code outside the Vue App must be **ES5** compatible.

======
Usage
======

Install it with ::

  pip install Flask-VueSFC


Here's an example on how to use the extension ::

  from flask_vue_sfc import VueSFC
  from flask_vue_sfc.helpers import render_vue_component, render_vue_page

  def create_app():
      app = Flask(__name__)

      VueSFC(app)

      @app.route('/example1')
      def example1():
          component = render_vue_component('index.vue')
          return render_template('example.html', component=component)

      @app.route('/example2')
      def example2():
          return render_vue_page('index.vue')

Since ``render_vue_component`` returns html syntax we need to make sure **jinja** doesn't try to
escape it. So be sure to always use the ``safe`` filter when rendering the component like so ::

    {{ component|safe }}


Feel free to checkout the examples folder for other examples.

Styling
-------
Sass styling is supported, though this needs to be tested in a complex app to determine the extent.

Escaping
--------
Occasionally, you might need a variable to be parsed by ``jinja`` instead of ``vue``. To achieve this, use triple
parenthesis i.e ``{{{ variable }}}``.

**Note:** Currently, escaping only supports root components.

Checkout **examples/app_with_escaping.py** for a sample.

--------------
Configuration
--------------
There are configuration options used by Flask-Vue-SFC.

+--------------------+------------------+-----------------------------------------------------------------------------+
|Option              | Default          |                                                                             |
+====================+==================+=============================================================================+
|VUE_USE_MINIFIED    | True             | Whether or not to use the minified scripts.                                 |
+--------------------+------------------+-----------------------------------------------------------------------------+
|VUE_PROD_MODE       | False            | If True, Vue components will be rendered when the extension is initialized. |
+--------------------+------------------+-----------------------------------------------------------------------------+
|VUE_SERVE_LOCAL     | False            | If True, scripts will be served from the local instance.                    |
+--------------------+------------------+-----------------------------------------------------------------------------+


A  ``cache`` instance MUST have the methods:
 - ``.get(key)``
 - ``.set(key, value, expires=None)``


==============================
Motivation?
==============================

Over the past year or so, I've found myself working on projects which involve Vue.js and Flask/Django.
In most scenarios the frontend app was a standalone application so a lot of thought didn't have to be put
into how it interacts with the backend besides through API calls. In some scenarios, however, the requirement
was usage of Vue.js as library instead of a framework. The latter pattern is becoming more common with the slow demise of **jQuery** (Yes, yes I said it :) )

Organizing Vue.js code becomes quite problematic due to the fact there's conventional way of organizing code when it's not
being used as a framework. Perhaps this is because it's all dependent on the backend framework being used and it's conventions.

Then it dawned unto me. What if devs could work with single file components directly without having to deal with webpack???

==============
Contributions
==============
All contributions are welcome. Feel feel free to raise an issue and open a PR if you want to fix a bug or add a feature.
