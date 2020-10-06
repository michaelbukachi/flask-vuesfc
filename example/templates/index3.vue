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
