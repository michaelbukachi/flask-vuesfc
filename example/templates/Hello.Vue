<template>
  <div class="example">{{ message }}</div>
</template>
<script>
export default  {
  name: 'Hello',
  data() {
    return {
      message: 'Hello'
    }
  }
}
</script>
<style>
.example {
  color: blue;
}
</style>