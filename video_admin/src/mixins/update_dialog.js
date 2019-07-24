const commonUpdateDialog = {
  data() {
    return {
    }
  },
  props: {
    visible: Boolean,
    data: Object,
    onCancel: Function,
    onOK: Function
  },
  methods: {
    handleCancel() {
      this.$emit('onCancel')
    },
    handleSubmit() {
      this.$emit('onOK', this.data)
    }
  }
}

export default commonUpdateDialog
