<template>
  <div class="example">{{ message }}</div>
  <div class="example">{{ anotherMessage }}</div>
  <hello></hello>
  <inner-hello></inner-hello>
</template>
<script>
import Hello from './Hello.Vue'
import InnerHello from './nested/InnerHello'

const foo = 'bar'


export default  {
  name: 'App',
  components: {
    Hello,
    InnerHello
  },
  data() {
    return {
      message: 'Vue example',
      anotherMessage: foo
    }
  }
}
</script>
<style>
.example {
  color: red
}

div {
  font-weight: bold;
}
</style>