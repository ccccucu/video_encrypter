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
          <div v-if="progressStatus.status === ''">视频加载中, 请稍后</div>
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
          prop="upload_organization.name"
          label="上传单位"
          sortable>
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
              :disabled="openIsDisabled"
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
  import {videoDownload, queryVideos, postWaterMark, get_uuid, pingServer} from '@/api/video'
  import FS from 'fs'
  import Path from 'path'
  import UserMixin from '@/mixins/UserMixin'
  import store from '@/store'
  export default {
    name: "index",
    mixins:[UserMixin],
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
        ping_server: undefined,
        ping_timer: 0,
        openIsDisabled: false,
        // videojs options
        videoPlayer: {
          src: ""
        },
        playerOptions: {

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
    beforeCreate(){

    },
    beforeDestroy() {
    clearInterval(this.ping_server);
    },
    created() {
      queryVideos({}).then((resp) => {
        this.tableData = resp.data.videos
        this.video_total = resp.data.total
      })
      this.$nextTick(()=>{
        this.addWaterMark()
      })
      this.ping_server = setInterval(()=>{
        pingServer().then(()=>{
          this.ping_timer = 0
        }).catch(()=>{
          this.ping_timer = this.ping_timer + 1
          if (this.ping_timer >= 3){
            this.player.reset()
          }
        })
      }, 4000)
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
        let str = this.userInfo.name;
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
        this.openIsDisabled = true
        // 点击播放按钮的回调
        this.player.reset()
        this.progressStatus.status = ''
        this.progressStatus.value = 0
        this.loading = true
        const video_name = row.uuid+'.mp4'
        const path = Path.resolve('./', video_name)
        const water_path = Path.resolve('./', 'water_'+this.userInfo.id.toString()+'_'+video_name)
        let writer = FS.createWriteStream(path)
        var respp_id
        this.progressStatus.value = 10

        if(FS.existsSync(water_path)){
            this.progressStatus.value = 100
            this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path, row.secret_key)
            this.player.load()
            //this.loading = false

        }else {
          // 下载视频
          videoDownload(row.id).then((download_resp) => {


            this.progressStatus.value = 30

            writer.on('finish', () =>{
              // 存入本地完成后 加水印                  
              let water_mark =  get_uuid()
              this.progressStatus.value = 50


              //50
                postWaterMark(row.id, water_mark).then((water_mark_resp) => {
                  this.progressStatus.value = 70

                  Rpc.clientReadVideo(path, row.secret_key, water_mark,water_path).then((client_read_vide_resp)=>{
                    this.openIsDisabled = false
                    this.progressStatus.value = 80
                    if (client_read_vide_resp.data.result) {

                        this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path, row.secret_key)
                        this.player.load()
                        this.loading = false

                    } else {
                      // 失败
                          this.progressStatus.status = 'exception'

                          this.$message({
                            type: 'error',
                            message: client_read_vide_resp.data.error.message
                          });
                    }
                  }).catch((err)=>{
                    this.openIsDisabled = false
                    var errtext = '加载失败，请检查网络环境';
                    // this.$message.error('服务器错误，请检查连接状态');
                    // alert(err);
                    this.$message({
                            type: 'info',
                            message: '视频加载失败，请重试'
                      });
                      this.progressStatus.value = 0
                      this.progressStatus.status = 'exception'
                  })
                })
            });

            download_resp.data.pipe(writer)
          }).catch((err) => {
            this.openIsDisabled = false
            debugger
          }).finally(()=>{
            //this.openIsDisabled = false
          });
        }
        //this.openIsDisabled = false
      }
    }
  }
</script>

<style>
.vjs-custom-skin > .video-js .vjs-tech {
  width: auto !important;
  height: auto !important;
  position: relative;
         
}
.vjs-custom-skin > .video-js {
  display: flex;
      justify-content: center;
    align-items: center;
   margin: 0 auto;
  font-family: "PingFang SC","Helvetica Neue","Hiragino Sans GB","Segoe UI","Microsoft YaHei","微软雅黑",sans-serif;
}

.vjs-custom-skin > .video-js .vjs-menu-button-inline.vjs-slider-active,.vjs-custom-skin > .video-js .vjs-menu-button-inline:focus,.vjs-custom-skin > .video-js .vjs-menu-button-inline:hover,.video-js.vjs-no-flex .vjs-menu-button-inline {
  width: 10em
}

.vjs-custom-skin > .video-js .vjs-controls-disabled .vjs-big-play-button {
  display: none!important
}

.vjs-custom-skin > .video-js .vjs-control {
  width: 3em
}

.vjs-custom-skin > .video-js .vjs-control.vjs-live-control{
  width: auto;
  padding-left: .5em;
  letter-spacing: .1em;
}

.vjs-custom-skin > .video-js .vjs-menu-button-inline:before {
  width: 1.5em
}

.vjs-menu-button-inline .vjs-menu {
  left: 3em
}

.vjs-paused.vjs-has-started.vjs-custom-skin > .video-js .vjs-big-play-button,.video-js.vjs-ended .vjs-big-play-button,.video-js.vjs-paused .vjs-big-play-button {
  display: block
}

.vjs-custom-skin > .video-js .vjs-load-progress div,.vjs-seeking .vjs-big-play-button,.vjs-waiting .vjs-big-play-button {
  display: none!important
}

.vjs-custom-skin > .video-js .vjs-mouse-display:after,.vjs-custom-skin > .video-js .vjs-play-progress:after {
  padding: 0 .4em .3em
}

.video-js.vjs-ended .vjs-loading-spinner {
  display: none;
}

.video-js.vjs-ended .vjs-big-play-button {
  display: block !important;
}

.video-js.vjs-ended .vjs-big-play-button,.video-js.vjs-paused .vjs-big-play-button,.vjs-paused.vjs-has-started.vjs-custom-skin > .video-js .vjs-big-play-button {
  display: none !important;
}

.vjs-custom-skin > .video-js .vjs-big-play-button {
  top: 50%;
  left: 50%;
  margin-left: -1.5em;
  margin-top: -1em
}

.vjs-custom-skin > .video-js .vjs-big-play-button {
  background-color: rgba(0,0,0,0.45);
  font-size: 3.5em;
  /*border-radius: 50%;*/
  height: 2em !important;
  line-height: 2em !important;
  margin-top: -1em !important
}

.video-js:hover .vjs-big-play-button,.vjs-custom-skin > .video-js .vjs-big-play-button:focus,.vjs-custom-skin > .video-js .vjs-big-play-button:active {
  background-color: rgba(36,131,213,0.9)
}

.vjs-custom-skin > .video-js .vjs-loading-spinner {
  border-color: rgba(36,131,213,0.8)
}

.vjs-custom-skin > .video-js .vjs-control-bar2 {
  background-color: #000000
}

.vjs-custom-skin > .video-js .vjs-control-bar {
  /*background-color: rgba(0,0,0,0.3) !important;*/
  color: #ffffff;
  font-size: 14px
}

.vjs-custom-skin > .video-js .vjs-play-progress,.vjs-custom-skin > .video-js  .vjs-volume-level {
  background-color: #2483d5
}

.vjs-custom-skin > .video-js .vjs-play-progress:before {
  top: -0.3em;
}

.vjs-custom-skin > .video-js .vjs-progress-control:hover .vjs-progress-holder {
  font-size: 1.3em;
}

.vjs-menu-button-popup.vjs-volume-menu-button-vertical .vjs-menu {
  left: 0em;
}

.vjs-custom-skin > .video-js .vjs-menu li {
  padding: 0;
  line-height: 2em;
  font-size: 1.1em;
  font-family: "PingFang SC","Helvetica Neue","Hiragino Sans GB","Segoe UI","Microsoft YaHei","微软雅黑",sans-serif;
}

.vjs-custom-skin > .video-js .vjs-time-tooltip,
.vjs-custom-skin > .video-js .vjs-mouse-display:after,
.vjs-custom-skin > .video-js .vjs-play-progress:after {
  border-radius: 0;
  font-size: 1em;
  padding: 0;
  width: 3em;
  height: 1.5em;
  line-height: 1.5em;
  top: -3em;
}

.vjs-custom-skin > .video-js .vjs-menu-button-popup .vjs-menu {
  width: 5em;
  left: -1em;
}

.vjs-custom-skin > .video-js .vjs-menu-button-popup.vjs-volume-menu-button-vertical .vjs-menu {
  left: 0;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-resolution-button .vjs-menu {
  /*order: 4;*/
}

/*排序顺序*/
.vjs-custom-skin > .video-js .vjs-control-bar .vjs-play-control {
  order: 0;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-time-control {
  min-width: 1em;
  padding: 0;
  margin: 0 .1em;
  text-align: center;
  display: block;
  order: 1;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-playback-rate .vjs-playback-rate-value{
  font-size: 1.2em;
  line-height: 2.4;
}

.vjs-custom-skin > .video-js .vjs-progress-control.vjs-control {
  order: 2;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-volume-menu-button {
  order: 3;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-resolution-button {
  order: 4;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-resolution-button .vjs-resolution-button-label {
  display: block;
  line-height: 3em;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-playback-rate {
  order: 5;
}

.vjs-custom-skin > .video-js .vjs-control-bar .vjs-fullscreen-control {
  order: 6;
}

</style>
