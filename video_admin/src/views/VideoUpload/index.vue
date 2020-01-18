<template>
  <div class="app-container">

    <el-form ref="form" label-width="80px" >
      <!--:model="form"-->
      <el-form-item label="视频标题:">
      <el-input v-model="query.title" placeholder="请输入视频标题"></el-input>
      </el-form-item>
      <el-form-item label="视频文件:" style="width: 500px">

      <el-upload
        class="upload-demo"
        ref="upload"
        drag
        :auto-upload="false"
        :headers ="upload_headers"
        action="/api/videos/upload"
        accept="audio/mp4,video/mp4"
        :on-success = "handleSuccess"
        :on-change= "handleFileChange"
        :multiple = "false"
      >

        <!--:file-list="uploadFileList"-->
        <img
          v-if="thumb_filename"
          width="100%"
          height="100%"
          class="el-upload-list__item-thumbnail"
          :src="videoThumbUrl" 
        >
        <div v-else>
            <i class="el-icon-upload"></i>
          <div class="el-upload__text">将视频拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传map4文件</div>
        </div>
      </el-upload>


      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitUpload">确认提交</el-button>
      </el-form-item>

    </el-form>


  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  //mixin
  import commonTable from '@/mixins/table'
  //视频接口
  import { queryVideos, deleteVideo, updateVideo, getVideo, createVideo,getVideoThumbPath } from '@/api/video'

  export default {
    mixins: [commonTable],
    data() {
      return {
        //配置minxin种curd api方法：
        newMethod: createVideo,
        deleteMethod: deleteVideo,
        updateMethod: updateVideo,
        getMethod: getVideo,
        queryMethod: queryVideos,

        //配置mixin query
        resource_name: 'video',

        data: [],  //视频列表

        query: {
            title: undefined
        },

        videoId: undefined,
        thumb_filename: ""

      }
    },
    computed: {
      ...mapGetters([
        'token',
      ]),

      videoThumbUrl() {
        return getVideoThumbPath(this.thumb_filename)
      }, 

      upload_headers(){
        return {
          'Authorization': 'Bearer ' + this.token
        }
      }
    },
    created() {
    },
    methods: {
      // 上传前改变文件名字
      handleFileChange(file, fileList) {
        debugger
          if (file.status === 'ready') {
            this.thumb_filename  = undefined
            this.query.title = file.raw.name
          }
      },

      //当文件上传成功后
      handleSuccess(response, file, fileList){
        var type = ''
        if (response.code == 200){
          type = response.status;
          this.videoId = response.id  //response.id    后端接口更新后会获得id
          console.log(response.msg)
          console.log("上传成功的视频id：" + response.id)
          this.thumb_filename = response.thumb_filename
          //上传信息
          updateVideo(this.videoId, this.query)


          this.$message({
            type: 'success',
            message: response.msg
          })
          // this.reload();

        } else {
          console.log(response.msg)
        }
        return type;
      },

      //点击提交 先上传文件，再上传信息
      submitUpload() {
        //1.上传视频
        this.$refs.upload.submit()
      },

    }
  }
</script>
