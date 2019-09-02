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
      <el-table :data="waterMarkInfo">
        <el-table-column prop="key" label="属性" width="180"></el-table-column>
        <el-table-column prop="value" label="值"></el-table-column>
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
      waterMarkInfo: [],
      fileList: [],
      loading: false
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
      this.loading = true
      Rpc.deWaterMarkByPath(this.current_file).then(resp => {
          this.loading = false
        if (resp.data.error) {
          // 出错
          this.$message({
            message: resp.data.error.message,
            type: "error"
          });
        } else {
          searchWaterMark(resp.data.result).then(search_resp => {
            if (search_resp.data.code === 200) {
            this.waterMarkInfo.push({
              key: "单位名称",
              value: this.search_resp.data.water_mark.organization_id
            });
            this.waterMarkInfo.push({
              key: "用户",
              value: this.search_resp.data.water_mark.user.name
            });
            this.waterMarkInfo.push({
              key: "ip",
              value: this.search_resp.data.water_mark.ip
            });
            this.waterMarkInfo.push({
              key: "视频标题",
              value: this.search_resp.data.water_mark.video.title
            });
            } else {
              this.$message('找不到水印对应记录， 请根据水印内容手动查找')
            }
          });
          this.waterMarkInfo.push({
            key: "原始内容",
            value: resp.data.result
          });
          console.log(resp);
        }
      });
    }
  }
};
</script>
