<template>
  <div class="example">{{ message }}</div>
</template>
<script>
export default  {
  name: 'InnerHello',
  data() {
    return {
      message: 'Inner Hello'
    }
  }
}
</script>
<style>
.example {
  color: green;
}
</style>