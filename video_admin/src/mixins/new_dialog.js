const commonNewDialog = {
  data() {
    return {
      data: null,
    }
  },
  props: {
    visible: Boolean,
    onCancel: Function,
    onOK: Function
  },
  methods: {
    handleCancel() {
      this.$emit('onCancel');
    },
    handleSubmit() {
      this.$emit('onOK', this.data);
    }
  }
}

export default commonNewDialog
