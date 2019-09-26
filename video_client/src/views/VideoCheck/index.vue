<template>
  <div class="app-container">
    <el-card
      v-loading="loading"
    element-loading-text="水印解析中"
    element-loading-spinner="el-icon-loading"
    >
      <div slot="header" class="clearfix">
        <span>水印解析</span>
      </div>
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="视频文件:">
          <el-upload
            class="upload-demo"
            drag
            action="/"
              :on-change="handleUpload"
            :file-list="fileList"
            :auto-upload="false"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将视频拖到此处，或
              <em>点击上传</em>
            </div>
            <div class="el-upload__tip" slot="tip">只能上传map4文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleParserClick">解析水印</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <div style="padding-top: 30px"></div>
    <el-card>
      <div slot="header" class="clearfix">
        <span>解析结果</span>
      </div>
      <el-table
        :data="water_marks">
        <el-table-column
          prop="id"
          label="编号"
          sortable
          width="80">
        </el-table-column>
        <el-table-column
          prop="watermark"
          label="水印"
          sortable
          width="180">
        </el-table-column>
        <el-table-column
          prop="video.title"
          label="视频标题"
          sortable>
        </el-table-column>
        <el-table-column
          prop="organization.name"
          label="单位"
          sortable>
        </el-table-column>
        <el-table-column
          prop="user.name"
          label="用户"
          sortable>
        </el-table-column>
        <el-table-column
          prop="ip"
          label="IP"
          sortable>
        </el-table-column>
        <el-table-column
          prop="time"
          label="时间"
          sortable>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import Rpc from "@/rpc/index";
import { searchWaterMark } from "@/api/video";

export default {
  data() {
    return {
      current_file: "",
      water_marks: [],
      raw : '',
      total :0,
      fileList: [],
      loading: false,
      frame : 0
    };
  },
  created() {},
  methods: {
    handleUpload(file, fileList) {
      // 上传新的文件的回调
      console.log(file);
      debugger
      this.fileList = []
      this.fileList = [file]
      this.current_file = file.raw.path;
    },
    handleParserClick() {
      this.waterMarkInfo = []
      if(this.current_file === ""){
        this.$message({
          message: "未选择文件",
          type: "error"
        });
        return false;
      }
      this.frame =0 
      this.parserSearchWaterMark()
     
    },
    parserSearchWaterMark(){
      this.loading = true
      return  Rpc.deWaterMarkByPath(this.current_file, this.frame).then(resp => {
        if (resp.data.error) {
          // 出错
          this.loading = false
          this.$message({
            message: resp.data.error.message,
            type: "error"
          });
        } else {
          this.raw = resp.data.result['contents']
          this.frame = resp.data.result['next_frame']
          searchWaterMark(this.raw).then(search_resp => {
            if (search_resp.data.code === 200) {
              this.loading = false
              this.water_marks = search_resp.data.water_marks
              this.total = search_resp.data.total
            } else {  
              this.parserSearchWaterMark()
            }
          });
          console.log(resp);
        }
      });
    }
  }
};
</script>
