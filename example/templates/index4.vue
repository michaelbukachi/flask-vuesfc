<template>
  <div>{{ message }}</div>
  <div>{{{ message }}}</div>
</template>
<script>

export default  {
  name: 'App',
  data() {
    return {
      message: 'This is rendered by Vue',
    }
  }
}
</script>