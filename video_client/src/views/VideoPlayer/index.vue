<template>
  <div>
    <el-card >
      <div  id="watermark-area">
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
        <div v-show="loading" style="text-align: center"  >
          <el-progress type="circle" :percentage="progressStatus.value" :status="progressStatus.status"></el-progress>
          <div v-if="progressStatus.status === ''">视频解密中, 请稍后</div>
          <div v-if="progressStatus.status === 'exception'">{{progressStatus.err}}</div>
        </div>
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
          height: '525',
          width: '1344',
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
      this.$nextTick(()=>{
        this.addWaterMark()
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
      watermark(str) {
        let can = document.createElement('canvas');
        let font_size = 40*(4/str.length);
        //设置画布的长宽
        can.width = font_size*str.length*2;
        can.height = font_size*str.length*2;
        let cans = can.getContext('2d');
        //旋转角度
        cans.rotate(-30 * Math.PI / 180);
        cans.font = font_size + 'pxa';
        //设置填充绘画的颜色、渐变或者模式
        cans.fillStyle = 'rgba(0,0,0,0.8)';
        //设置文本内容的当前对齐方式
        cans.textAlign = 'left';
        //设置在绘制文本时使用的当前文本基线
        cans.textBaseline = 'Middle';
        //在画布上绘制填色的文本（输出的文本，开始绘制文本的X坐标位置，开始绘制文本的Y坐标位置）
        cans.fillText(str, 0, font_size*str.length);
        let background = 'url(' + can.toDataURL('image/png') + ') left top repeat';
        return background;
      },
      addWaterMark() {
        let ct_element = document.getElementById('watermark-area');
        let str = '121.56.29.239';
        if(str){
          let bg = this.watermark(str);
          ct_element.style.background = bg;
        }
      },
      handleVideoError(event) {
        console.log(event)

      },
      handleDurationChange(event) {
        console.log(event)
      },
      handleListPlayClick(row) {
        // 点击播放按钮的回调
        this.loading = true
        const video_name = row.uuid+'.mp4'
        const path = Path.resolve('./', video_name)
        const writer = FS.createWriteStream(path)
        this.progressStatus.value = 10
        // 下载视频
        videoDownload(row.id).then((resp) => {
          this.progressStatus.value = 30
          writer.on('finish', () => {
            // 存入本地完成后 加水印
            this.progressStatus.value = 50
            const water_path = Path.resolve('./', 'water_'+video_name)
            Rpc.clientReadVideo(path, row.secret_key,'121.56.29.239',water_path).then((resp)=>{
              if (resp.data.result) {
                // 加水印成功
                this.progressStatus.value = 100
                this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path)
                this.player.load()
                console.log(this.player)
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
