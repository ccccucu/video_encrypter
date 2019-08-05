<template>
  <div class="app-container">
    <el-card>
      <div
        v-show="!loading"
        class="player"
        style="text-align: center; width: 100%">
        <video-player  class="vjs-custom-skin"
                       ref="videoPlayer"
                       :options="playerOptions"
                       :playsinline="true">
        </video-player>
      </div>
      <div v-show="loading" style="text-align: center">
        <el-progress type="circle" :percentage="progressStatus.value" :status="progressStatus.status"></el-progress>
        <div v-if="progressStatus.status === ''">视频解密中, 请稍后</div>
        <div v-if="progressStatus.status === 'exception'">{{progressStatus.err}}</div>
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
        // 进度条:
        progressStatus: {
          value: 0,
          status: '',
          err: 'ERROR'
        },
        // videojs options
        videoPlayer: {
          src: ""
        },
        playerOptions: {
          height: '360',
          autoplay: true,
          muted: false,
          language: 'en',
          playbackRates: [0.7, 1.0, 1.5, 2.0],
          sources: [{
            type: "video/mp4",
            // mp4
            src: "",
            // webm
            // src: "https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm"
          }],
          poster: "",
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
      player() {
        return this.$refs.videoPlayer.player
      }
    },
    methods: {
      handleVideoError(event) {
        console.log(event)

      },
      handleDurationChange(event) {
        console.log(event)
      },
      handleListPlayClick(row) {
        // 点击播放按钮的回调
        this.loading = true
        const path = Path.resolve('./', row.uuid)
        const writer = FS.createWriteStream(path)
        this.progressStatus.value = 10
        // 下载视频
        videoDownload(row.id).then((resp) => {
          this.progressStatus.value = 30
          writer.on('finish', () => {
            // 存入本地完成后 加水印
            this.progressStatus.value = 50
            const water_path = Path.resolve('./', 'water_'+row.uuid)
            Rpc.enWaterMarkByPath(path, 'test',water_path).then((resp)=>{
              if (resp.data.result) {
                // 加水印成功
                this.progressStatus.value = 100
                this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path)
                this.player.load()
                this.loading = false
              } else {
                // 失败
                this.progressStatus.status = 'exception'
              }
            })
          });
          resp.data.pipe(writer)
        }).catch((err) => {
          debugger
        });
      }
    }
  }
</script>

<style>

</style>
