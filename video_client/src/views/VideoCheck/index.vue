<template>
  <div class="app-container">
    <el-card>
      <div slot="header" class="clearfix">
        <span>水印解析</span>
      </div>
      <el-form ref="form" :model="form" label-width="80px">
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
          <el-button type="primary">解析水印</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  <div style="padding-top: 30px"></div>
    <el-card>
      <div slot="header" class="clearfix">
        <span>解析结果</span>
      </div>
      <el-table
        :data="tableData">
        <el-table-column
          prop="key"
          label="属性"
          width="80">
        </el-table-column>
        <el-table-column
          prop="value"
          label="值"
          width="180">
        </el-table-column>
      </el-table>
    </el-card>

  </div>
</template>

<script>

  export default {
    data() {
      return {
        tableData: [
          {
            key: 'IP',
            value: '0.0.0.0',
          },
          {
            key: '用户',
            value: '测试用户',
          }
        ]
      }
    },
    created() {
    },
    methods: {}
  }
</script>
