<template>
  <div>
    <svgIcon v-if="icon" :name="icon" style="font-size: 1.6em;padding-right: 3px"/>
    <span v-if="title" slot="title">{{title}}</span>
  </div>
</template>
<script>
import svgIcon from '@/components/SvgIcon'
export default {
  name: 'MenuItem',
  components: { svgIcon },
  props: {
    icon: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    }
  },
}
</script>
