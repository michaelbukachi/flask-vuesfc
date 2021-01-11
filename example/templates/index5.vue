<template>
  <div class="a">
    <div class="b">{{ message }}</div>
  </div>
</template>
<script>

export default  {
  name: 'App',
  data() {
    return {
      message: 'This is a styled message',
    }
  }
}
</script>
<style lang="scss">
.a {
  font-weight: bold;
  .b {
    color: red;
  }
}
</style>