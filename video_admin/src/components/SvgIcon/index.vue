<template>
  <i :class="svgClass" style="
    width: 1em;
    height: 1em;
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
   "></i>
</template>

<script>
  export default {
    name: 'SvgIcon',
    props: {
      name: {
        type: String,
        default: ''
      }
    },
    computed: {
      svgClass() {
        if (this.name) {
          return 'iconfont ' + this.name
        } else {
          return 'iconfont'
        }
      }
    }
  }
</script>

<style scoped>

</style>
