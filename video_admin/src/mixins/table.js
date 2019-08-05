const commonTable = {
  data() {
    return {
      resource_name: 'data', //资源名称 比如 Video表 resource_name = ‘video’
      data: [],  //响应数据种的data参数，
      total: 0, //返回查询到的条数
      pages: { _page: 1, _per_page: 30 }, //翻页 _page 第几页，  _per_page 每页几条数据
      query: {},  //查询时所需要的条件dict
      order: { _order_by: 'id', _desc: true }, //排序相关内容
      selected_data: {},  //编辑表单种 选中编辑的对象dict

      updateDialogShow: false, //更新对话框显示
      newDialogShow: false,  //新增对话框显示

      tableLoading: false,  //数据列表加载状态

      newMethod: null,  //新增api函数
      deleteMethod: null,  //删除api函数
      updateMethod: null,  //跟新api函数
      getMethod: null,  //获取一条记录api函数
      queryMethod: null  //批量查询api函数
    }
  },
  methods: {
    //res 是 axios 的请求对象， data 是响应内容
    //批量查询列表
    fetchData() {
      this.tableLoading = true
      let params = { ...this.query, ...this.pages, ...this.order }
      return this.queryMethod(params).then((res) => {
        this.total = res.data.total
        this.updateLocal(res.data)
        this.tableLoading = false
      })
    },
    //将 "批量查询列表" 方法中 返回的列表数据更新到本地
    updateLocal(data) {
      this.data = data[this.resource_name + 's']
    },
    //翻页 或 跳转页数
    onPageChange(page) {
      this.pages._page = page
      this.fetchData()
    },
    //条件查询框中：点击查询按钮
    onSearch() {
      this.pages._page = 1
      this.fetchData()
    },
    //条件查询框中：重置按钮
    onReset() {
      this.query = {}
      this.order = { _order_by: 'id', _desc: true }
      this.pages._page = 1
      this.fetchData()
    },
    //table组件中 @sort-change="onSort" ， table-column 可增添‘sortable’参数 使列表可排序
    onSort(args) {
      this.pages._page = 1
      if (args.prop) {
        this.order = { _order_by: args.prop, _desc: args.order === 'descending' }
      } else {
        this.order = { _order_by: 'id', _desc: true }
      }
      this.fetchData()
    },
    //打开更新数据对话框
    onUpdateClick(index, row) {
      this.getMethod(row.id).then((resp) => {
        this.selected_data = resp.data[this.resource_name]
      })
      this.updateDialogShow = true
    },
    //单条数据更新
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
    //关闭更新数据对话框
    onUpdateCancel() {
      this.updateDialogShow = false
    },
    //打开新增数据对话框
    onNewClick() {
      this.newDialogShow = true
    },
    //新增一条数据
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
    //关闭新增数据对话框
    onNewCancel() {
      this.newDialogShow = false
    },
    //删除一条数据
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
