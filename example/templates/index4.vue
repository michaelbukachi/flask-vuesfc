<template>
  <div>{{ message }}</div>
  <div>{{{ message }}}</div>
  <inner-escaping></inner-escaping>
</template>
<script>
import InnerEscaping from "./nested/InnerEscaping";

export default  {
  name: 'App',
  components: {InnerEscaping},
  data() {
    return {
      message: 'This is rendered by Vue',
    }
  }
}
</script>