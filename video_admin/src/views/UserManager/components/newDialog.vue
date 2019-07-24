<template>
  <el-dialog title="添加模板" :visible="visible" @close="handleCancel">
    <el-form :model="data" label-width="80px" ref="templateForm">
      <el-form-item label="标题" prop="title">
        <el-input v-model="data.title"></el-input>
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input   type="textarea"
                    placeholder="请输入内容"
                  :autosize="{ minRows: 2, maxRows: 10}"
              v-model="data.content"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import commonNewDialog from '@/mixins/new_dialog'

export default {
  mixins: [commonNewDialog],
  data() {
    return {
      data: {
        title:'',
        content:''
      }
    }
  }
}
</script>
