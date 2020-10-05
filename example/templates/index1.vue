<template>
  <div class="example">{{ message }}</div>
</template>
<script>
export default  {
  name: 'App',
  data() {
    return {
      message: 'Vue example'
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