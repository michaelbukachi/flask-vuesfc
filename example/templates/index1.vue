<template>
  <div class="example">{{ message }}</div>
  <div class="example">{{ anotherMessage }}</div>
</template>
<script>
const foo = 'bar'


export default  {
  name: 'App',
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