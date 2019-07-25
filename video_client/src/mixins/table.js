const commonTable = {
  data() {
    return {
      resource_name: 'data',
      data: [],
      total: 0,
      pages: { _page: 1, _per_page: 30 },
      query: {},
      order: { _order_by: 'id', _desc: true },
      selected_data: {},

      updateDialogShow: false,
      newDialogShow: false,

      tableLoading: false,

      newMethod: null,
      deleteMethod: null,
      updateMethod: null,
      getMethod: null,
      queryMethod: null
    }
  },
  methods: {
    fetchData() {
      this.tableLoading = true
      let params = { ...this.query, ...this.pages, ...this.order }
      return this.queryMethod(params).then((res) => {
        this.total = res.data.total
        this.updateLocal(res.data)
        this.tableLoading = false
      })
    },
    updateLocal(data) {
      this.data = data[this.resource_name + 's']
    },
    onPageChange(page) {
      this.pages._page = page
      this.fetchData()
    },
    onSearch() {
      this.pages._page = 1
      this.fetchData()
    },
    onReset() {
      this.query = {}
      this.order = { _order_by: 'id', _desc: true }
      this.pages._page = 1
      this.fetchData()
    },
    onSort(args) {
      this.pages._page = 1
      if (args.prop) {
        this.order = { _order_by: args.prop, _desc: args.order === 'descending' }
      } else {
        this.order = { _order_by: 'id', _desc: true }
      }
      this.fetchData()
    },
    onUpdateClick(index, row) {
      this.getMethod(row.id).then((resp) => {
        this.selected_data = resp.data[this.resource_name]
      })
      this.updateDialogShow = true
    },
    onUpdateOK(obj) {
      this.updateMethod(this.selected_data.id, obj).then((res) => {
        if (res.data.code === 200) {
          this.updateDialogShow = false
          this.$message({
            type: 'success',
            message: '修改成功'
          })
          return this.fetchData()
        }
      })
    },
    onUpdateCancel() {
      this.updateDialogShow = false
    },
    onNewClick() {
      this.newDialogShow = true
    },
    onNewOK(obj) {
      this.newMethod(obj).then((res) => {
        if (res.data.code === 200) {
          this.newDialogShow = false
          this.$message({
            type: 'success',
            message: '创建成功'
          })
          return this.fetchData()
        }
      })
    },
    onNewCancel() {
      this.newDialogShow = false
    },
    onDeleteClick(index, row) {
      this.$confirm('确认删除？').then(() => {
        this.deleteMethod(row.id).then(res => {
          if (res.data.code === 200) {
            this.$message({
              type: 'success',
              message: '删除成功'
            })
          }
          this.fetchData()
        })
      })
    }
  },
  mounted() {
    this.fetchData()
  }
}

export default commonTable
