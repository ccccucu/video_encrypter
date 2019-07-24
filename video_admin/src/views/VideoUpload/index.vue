<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="视频标题:">
      <el-input v-model="input" placeholder="请输入视频标题"></el-input>
      </el-form-item>
      <el-form-item label="视频文件:">
      <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将视频拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传map4文件</div>
      </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">确认提交</el-button>
        <el-button type="danger">取消提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

  export default {
    data() {
      return {}
    },
    created() {
    },
    methods: {}
  }
</script>
