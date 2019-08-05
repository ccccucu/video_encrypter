<template>
  <div class="app-container">
    <el-card>
      <div
        v-if="!loading"
        class="player"
        style="text-align: center; width: 100%">
        <video style="width: 100%"
               :src="video_player.src"
               controls="controls"
        > </video>
      </div>
      <div v-else style="text-align: center">
        <el-progress type="circle" :percentage="25"></el-progress>
        <div>视频解密中, 请稍后</div>
      </div>
    </el-card>
    <div style="padding-top: 30px"></div>
    <el-card>
      <el-table
        :data="tableData" max-height="500">
        <el-table-column
          prop="id"
          label="编号"
          width="80">
        </el-table-column>
        <el-table-column
          prop="title"
          label="标题"
          width="180">
        </el-table-column>
        <el-table-column
          prop="upload_unit"
          label="上传单位">
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="上传时间">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="handleListPlayClick(scope.row)"
            >播放
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

  </div>
</template>

<script>
  import 'video.js/dist/video-js.css'
  import './style.css'
  import Rpc from '@/rpc/index'
  import {videoDownload, queryVideos} from '@/api/video'
  import FS from 'fs'
  import Path from 'path'

  export default {
    name: "index",

    data() {
      return {
        loading: false,
        tableData: [],
        video_total: 0,
        // videojs options
        video_player: {
          src: ''
        }
      }
    },
    created() {
      queryVideos({}).then((resp) => {
        this.tableData = resp.data.videos
        this.video_total = resp.data.total
      })
    },
    mounted() {
      },
    computed: {

    },
    methods: {

      handleListPlayClick(row) {
        // 点击播放按钮的回调
        this.loading = true
        const path = Path.resolve('./', row.uuid)
        const writer = FS.createWriteStream(path)
        videoDownload(row.id).then((resp) => {
          resp.data.pipe(writer)
          this.video_player.src = Rpc.readLocalUrl(path)
          this.loading = false
        }).catch((err) => {
        });
      }
    }
  }
</script>

<style>

</style>
