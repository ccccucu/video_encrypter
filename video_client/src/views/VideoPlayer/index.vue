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
    beforeCreate(){

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
        pingServer().catch(()=>{
          this.playerOptions.sources[0].src = ''
          this.player.load()
          this.player.stop()
        })
      }, 3000)
      setInterval(()=>{
        Rpc.Ping(path).catch((err)=>{
          this.player.stop()
          this.$message.error('本地服务错误，请检查系统状态');
        })
      }, 2630)
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
        // 点击播放按钮的回调
        this.progressStatus.status = ''
        this.progressStatus.value = 0
        this.loading = true
        const video_name = row.uuid+'.mp4'
        const path = Path.resolve('./', video_name)
        const water_path = Path.resolve('./', 'water_'+video_name)
        let writer = FS.createWriteStream(path)
        var respp_id
        this.progressStatus.value = 10

        if(FS.existsSync(water_path)){
            this.progressStatus.value = 100
            this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path, row.secret_key)
            this.player.load()
            this.loading = false
        }else {
          // 下载视频
          videoDownload(row.id).then((download_resp) => {
            this.progressStatus.value = 30

            writer.on('finish', () =>{
              // 存入本地完成后 加水印                  
              let water_mark =  get_uuid()
              this.progressStatus.value = 50

              //50%
              setTimeout(()=>{
                postWaterMark(row.id, water_mark).then((water_mark_resp) => {
                  this.progressStatus.value = 70

                  Rpc.clientReadVideo(path, row.secret_key, water_mark,water_path).then((client_read_vide_resp)=>{

                    this.progressStatus.value = 80

                    if (client_read_vide_resp.data.result) {

                      setTimeout(()=>{
                        this.progressStatus.value = 100
                        this.progressStatus.status = "success"
                      },100)

                      setTimeout(()=>{
                        // 加水印成功
                        this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path, row.secret_key)
                        this.player.load()
                        this.loading = false
                      },600)

                    } else {
                      // 失败
                      this.progressStatus.status = 'warning'
                    }
                  }).catch((err)=>{
                    var errtext = '加载失败，请检查网络环境';
                    // this.$message.error('服务器错误，请检查连接状态');
                    // alert(err);
                    this.$alert(errtext, '读取失败', {
                      confirmButtonText: '确定',
                      callback: action => {
                        this.$message({
                          type: 'info',
                          message: `action: ${action}`
                        });
                      }
                    });

                    // this.progressStatus.value = 0
                    this.progressStatus.status = 'exception'
                  }).finally(()=>{

                  })
                })
              },800)


              // postWaterMark(row.id, water_mark).then((water_mark_resp) => {
              //   this.progressStatus.value = 70
              //
              //     Rpc.clientReadVideo(path, row.secret_key, water_mark,water_path).then((client_read_vide_resp)=>{
              //
              //       this.progressStatus.value = 80
              //
              //       if (client_read_vide_resp.data.result) {
              //         this.progressStatus.value = 100
              //         this.progressStatus.status = "success"
              //
              //         setTimeout(()=>{
              //           // 加水印成功
              //           this.playerOptions.sources[0].src = Rpc.readLocalUrl(water_path, row.secret_key)
              //           this.player.load()
              //           this.loading = false
              //         },600)
              //
              //       } else {
              //         // 失败
              //         this.progressStatus.value = 0
              //         this.progressStatus.status = 'warning'
              //       }
              //     })
              // })
            });

            download_resp.data.pipe(writer)
          }).catch((err) => {
            debugger
          });
        }
      }
    }
  }
</script>

<style>

</style>
