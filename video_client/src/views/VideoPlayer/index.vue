<template>
  <div>
    <el-card>
      <div id="watermark-area">
        <div
          v-show="this.fsm.state === this.PLAYER_STATUS.PLAYING"
          class="player"
          style="text-align: center; width: 100%"
        >
          <video-player
            class="vjs-custom-skin"
            ref="videoPlayer"
            @fullscreenchange="hanleFullScreenChange"
            :events="videoEvent"
            :options="playerOptions"
            :playsinline="false"
          ></video-player>
        </div>
        
        <div
          v-show="show_progess"
          v-loading="progess_loading"
          :element-loading-text="loading_text"
          element-loading-background="rgba(0, 0, 0, 0.8)"
          style="text-align: center;min-height:220px"
        >
          <el-progress
            v-show="!progess_loading"
            type="circle"
            :percentage="progressStatus.value"
            :status="progressStatus.status"
          ></el-progress>
          <div v-show="!progess_loading" v-if="progressStatus.status === 'exception'">{{err_msg}}</div>
          <div v-show="!progess_loading" v-if="progressStatus.status === 'success'">文件到导出出成功</div>
        </div>

      </div>
    </el-card>
    <div style="padding-top: 30px"></div>
    <el-card>
      <el-table :data="tableData" max-height="500">
        <el-table-column prop="id" label="编号" width="80"></el-table-column>
        <el-table-column prop="title" label="标题" width="180"></el-table-column>
        <el-table-column prop="upload_organization.name" label="上传单位" sortable></el-table-column>
        <el-table-column prop="created_at" label="上传时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleListPlayClick(scope.row)">播放</el-button>
            <el-button size="mini" type="primary" @click="handleListExportingClick(scope.row)">下载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import Rpc from "@/rpc/index";
import {
  videoDownload,
  queryVideos,
  postWaterMark,
  get_uuid,
  pingServer
} from "@/api/video";
import FS from "fs";
import Path from "path";
import UserMixin from "@/mixins/UserMixin";
import store from "@/store";
const { ipcRenderer } = require("electron");
const { dialog } = require("electron").remote;
import { PLAYER_STATUS, PING_MAX_TIME, DOWNLOAD_WAY } from "./const";
import StateMachine from "javascript-state-machine";

export default {
  name: "index",
  mixins: [UserMixin],
  data() {
    return {
      tableData: [],
      video_total: 0,

      ping_server: undefined,
      ping_timer: 0,

      fsm: undefined,
      PLAYER_STATUS: PLAYER_STATUS,

      progressStatus : {
          value: 100,
          status: 'success'
      },
      err_msg: "",

      download_way: DOWNLOAD_WAY.PLAYING, // 下载是为了

      current_video: undefined, //当前video

      export_path: "",

      videoEvent: ["fullscreenchange"],
      playerOptions: {
        width: 290,
        autoplay: true,
        muted: false,
        language: "en",
        sources: [
          {
            type: "video/mp4",
            // mp4
            src: ""
            // webm
            // src: "https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm"
          }
        ],
        poster: ""
      }
    };
  },

  computed: {
    player() {
      return this.$refs.videoPlayer.player;
    },

    video_path_info: function() {
      // video 的路径
      let res = {
        video_file: "",
        video_path: "",
        en_water_path: "",
        raw_water_path: ""
      };
      if (this.current_video) {
        const video_file = this.current_video.uuid + ".mp4";
        res.video_file = video_file;
        res.video_path = Path.resolve("./", video_file);
        res.en_water_path = Path.resolve(
          "./",
          "water_" + this.userInfo.id.toString() + "_" + video_file
        );
        res.raw_water_path = Path.resolve(
          "./",
          "raw_water_" + this.userInfo.id.toString() + "_" + video_file
        );
      }
      return res;
    },

    show_progess: function() {
      // 控制区域是否在显示
      if (this.fsm.state === PLAYER_STATUS.NORMAL || this.fsm.state === PLAYER_STATUS.PLAYING) {
        return false
      } 
      return true
    },

    progess_loading: function() {
      // 控制区域是否在加载
      if(this.fsm.state === this.PLAYER_STATUS.DOWNLOADING || this.fsm.state === PLAYER_STATUS.PROCESSING) {
        return true
      }
      return false
    },

    loading_text: function() {
      // 加载中的文字
      if (this.fsm.state === this.PLAYER_STATUS.DOWNLOADING) {
        return "视频下载中， 请稍后....."
      } else if (this.fsm.state === this.PLAYER_STATUS.PROCESSING) {
        return "视频加载中， 请稍后...."
      } 
      return "未知状态"
    }
    
    
  },

  beforeCreate() {},
  beforeDestroy() {
    clearInterval(this.ping_server);
  },
  created() {
    this.fsm = new StateMachine({
      init: this.PLAYER_STATUS.NORMAL,
      transitions: [
        {
          name: "Download",
          from: [
            this.PLAYER_STATUS.NORMAL,
            this.PLAYER_STATUS.PLAYING,
            this.PLAYER_STATUS.FAILED,
            this.PLAYER_STATUS.ERROR
          ],
          to: this.PLAYER_STATUS.DOWNLOADING
        },
        {
          name: "Process",
          from: this.PLAYER_STATUS.DOWNLOADING,
          to: this.PLAYER_STATUS.PROCESSING
        },
        {
          name: "Fail",
          from: [this.PLAYER_STATUS.DOWNLOADING, this.PLAYER_STATUS.PROCESSING],
          to: this.PLAYER_STATUS.FAILED
        },
        { name: "Error", from: "*", to: this.PLAYER_STATUS.ERROR },
        {
          name: "Success",
          from: [this.PLAYER_STATUS.EXPORTING],
          to: this.PLAYER_STATUS.SUCCESS
        },
        {
          name: "Play",
          from: [this.PLAYER_STATUS.PROCESSING, this.PLAYER_STATUS.NORMAL],
          to: this.PLAYER_STATUS.PLAYING
        },
        {
          name: "Export",
          from: [this.PLAYER_STATUS.PROCESSING, this.PLAYER_STATUS.NORMAL,  this.PLAYER_STATUS.PLAYING ],
          to: this.PLAYER_STATUS.EXPORTING
        }
      ],

      methods: {
        onError: ()=>{},
        onDownload: () => {
          return this.handleDownLoad();
        },

        onProcess: () => {
          return this.handleProcessing();
        },

        onPlay: ()=> {
          this.handlePlaying()
        },

        onFail: () =>{
          this.progressStatus.status = "exception"
        },

        onSuccess: () =>{
          this.progressStatus.status = "success"
        },

        onExport: ()=>{
          return this.handleExporting()
        },

        onInvalidTransition: function(transition, from, to) {
          debugger
         }
      }
    });

    queryVideos({}).then(resp => {
      this.tableData = resp.data.videos;
      this.video_total = resp.data.total;
    });

    this.ping_server = setInterval(() => {
      pingServer()
        .then(() => {
          // 收到正确响应回复
          this.ping_timer = 0;
        })
        .catch(() => {
          // 连续超时三次任务
          this.ping_timer = this.ping_timer + 1;
          if (this.ping_timer >= 3) {
            this.player.reset();
          }
        });
    }, 4000);
  },
  mounted() {
    this.$nextTick(() => {
      this.addWaterMark();
    });
  },
  methods: {
    // 状态机 downloading
    handleDownLoad() {
      let writer = FS.createWriteStream(this.video_path_info.video_path);
      videoDownload(this.current_video.id)
        .then(download_resp => {
          writer.on("finish", () => {
            this.fsm.process();
          });
          download_resp.data.pipe(writer);
        })
        .catch(() => {
          this.fsm.fail();
        });
    },

    // 状态机 processing
    handleProcessing() {
      return postWaterMark(this.current_video.id)
        .then(water_mark_resp => {
          let water_mark = get_uuid();
          Rpc.clientReadVideo(
            this.video_path_info.video_path,
            this.current_video.secret_key,
            water_mark,
            this.video_path_info.en_water_path,
            this.userInfo.id.toString()
          )
            .then(client_read_vide_resp => {
              if (client_read_vide_resp.data.result) {
                if (this.download_way === DOWNLOAD_WAY.PLAYING) {
                  this.fsm.play();
                } else if (this.download_way === DOWNLOAD_WAY.EXPORTING) {
                  this.fsm.export();
                }
              } else {
                // 失败
                debugger
                this.err_msg = client_read_vide_resp.data.error.message;
                this.fsm.fail();
              }
            })
            .catch(err => {
              debugger
              this.err_msg = "本地读取失败";
              this.fsm.fail();
            });
        })
        .catch(err => {
          debugger
          this.err_msg = "服务器申请水印错误";
          this.fsm.fail();
        });
    },

    // 状态机 playing
    handlePlaying() {
      this.playerOptions.sources[0].src = Rpc.readLocalUrl(
        this.video_path_info.raw_water_path,
        this.current_video.secret_key
      );
      this.player.load();
    },

    // 状态机 
    handleExporting() {
      FS.copyFileSync(raw_water_path, save_path);
      this.$message({
                type: 'success',
                message: '文件导出成功'
      });
      this.fsm.success()
    },

    hanleFullScreenChange(event) {
      ipcRenderer.send("setFullScreen", { flag: event.isFullscreen_ });
    },
    watermark(str) {
      let can = document.createElement("canvas");
      let font_size = 40 * (4 / str.length);
      //设置画布的长宽
      can.width = font_size * str.length * 2;
      can.height = font_size * str.length * 2;
      let cans = can.getContext("2d");
      //旋转角度
      cans.rotate((-30 * Math.PI) / 180);
      cans.font = font_size + "pxa";
      //设置填充绘画的颜色、渐变或者模式
      cans.fillStyle = "rgba(0,0,0,0.8)";
      //设置文本内容的当前对齐方式
      cans.textAlign = "left";
      //设置在绘制文本时使用的当前文本基线
      cans.textBaseline = "Middle";
      //在画布上绘制填色的文本（输出的文本，开始绘制文本的X坐标位置，开始绘制文本的Y坐标位置）
      cans.fillText(str, 0, font_size * str.length);
      let background =
        "url(" + can.toDataURL("image/png") + ") left top repeat";
      return background;
    },
    addWaterMark() {
      let ct_element = document.getElementById("watermark-area");
      let str = this.userInfo.name;
      if (str) {
        let bg = this.watermark(str);
        ct_element.style.background = bg;
      }
    },
    handleVideoError(event) {
      console.log(event);
    },
    handleDurationChange(event) {
      console.log(event);
    },
    handleListPlayClick(row) {
      this.current_video = row;
      this.download_way = DOWNLOAD_WAY.PLAYING;
      if(FS.existsSync(this.video_path_info.raw_water_path)){
        this.fsm.play()
      } else {
        this.fsm.download();
      }
    },
    handleListExportingClick(row) {
      this.current_video = row;
      this.download_way = DOWNLOAD_WAY.EXPORTING;

      let save_path = dialog.showSaveDialog({
        filters: [{ name: "Movies", extensions: ["mp4"] }]
      });
      this.export_path = save_path

      if (save_path) {

        if(FS.existsSync(this.video_path_info.raw_water_path)){
          this.fsm.export()
        } else {
          this.fsm.download();
        }
      }
    }
  }
};
</script>

<style>
.vjs-custom-skin > .video-js .vjs-tech {
  width: 100%;
  height: 100%;
  position: relative;
}

.vjs-custom-skin > .vjs-fullscreen > .vjs-tech {
  position: relative;
}
.vjs-custom-skin > .video-js {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  font-family: "PingFang SC", "Helvetica Neue", "Hiragino Sans GB", "Segoe UI",
    "Microsoft YaHei", "微软雅黑", sans-serif;
}

.vjs-custom-skin > .video-js .vjs-menu-button-inline.vjs-slider-active,
.vjs-custom-skin > .video-js .vjs-menu-button-inline:focus,
.vjs-custom-skin > .video-js .vjs-menu-button-inline:hover,
.video-js.vjs-no-flex .vjs-menu-button-inline {
  width: 10em;
}

.vjs-custom-skin > .video-js .vjs-controls-disabled .vjs-big-play-button {
  display: none !important;
}

.vjs-custom-skin > .video-js .vjs-control {
  width: 3em;
}

.vjs-custom-skin > .video-js .vjs-control.vjs-live-control {
  width: auto;
  padding-left: 0.5em;
  letter-spacing: 0.1em;
}

.vjs-custom-skin > .video-js .vjs-menu-button-inline:before {
  width: 1.5em;
}

.vjs-menu-button-inline .vjs-menu {
  left: 3em;
}

.vjs-paused.vjs-has-started.vjs-custom-skin > .video-js .vjs-big-play-button,
.video-js.vjs-ended .vjs-big-play-button,
.video-js.vjs-paused .vjs-big-play-button {
  display: block;
}

.vjs-custom-skin > .video-js .vjs-load-progress div,
.vjs-seeking .vjs-big-play-button,
.vjs-waiting .vjs-big-play-button {
  display: none !important;
}

.vjs-custom-skin > .video-js .vjs-mouse-display:after,
.vjs-custom-skin > .video-js .vjs-play-progress:after {
  padding: 0 0.4em 0.3em;
}

.video-js.vjs-ended .vjs-loading-spinner {
  display: none;
}

.video-js.vjs-ended .vjs-big-play-button {
  display: block !important;
}

.video-js.vjs-ended .vjs-big-play-button,
.video-js.vjs-paused .vjs-big-play-button,
.vjs-paused.vjs-has-started.vjs-custom-skin > .video-js .vjs-big-play-button {
  display: none !important;
}

.vjs-custom-skin > .video-js .vjs-big-play-button {
  top: 50%;
  left: 50%;
  margin-left: -1.5em;
  margin-top: -1em;
}

.vjs-custom-skin > .video-js .vjs-big-play-button {
  background-color: rgba(0, 0, 0, 0.45);
  font-size: 3.5em;
  /*border-radius: 50%;*/
  height: 2em !important;
  line-height: 2em !important;
  margin-top: -1em !important;
}

.video-js:hover .vjs-big-play-button,
.vjs-custom-skin > .video-js .vjs-big-play-button:focus,
.vjs-custom-skin > .video-js .vjs-big-play-button:active {
  background-color: rgba(36, 131, 213, 0.9);
}

.vjs-custom-skin > .video-js .vjs-loading-spinner {
  border-color: rgba(36, 131, 213, 0.8);
}

.vjs-custom-skin > .video-js .vjs-control-bar2 {
  background-color: #000000;
}

.vjs-custom-skin > .video-js .vjs-control-bar {
  /*background-color: rgba(0,0,0,0.3) !important;*/
  color: #ffffff;
  font-size: 14px;
}

.vjs-custom-skin > .video-js .vjs-play-progress,
.vjs-custom-skin > .video-js .vjs-volume-level {
  background-color: #2483d5;
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
  font-family: "PingFang SC", "Helvetica Neue", "Hiragino Sans GB", "Segoe UI",
    "Microsoft YaHei", "微软雅黑", sans-serif;
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

.vjs-custom-skin
  > .video-js
  .vjs-menu-button-popup.vjs-volume-menu-button-vertical
  .vjs-menu {
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
  margin: 0 0.1em;
  text-align: center;
  display: block;
  order: 1;
}

.vjs-custom-skin
  > .video-js
  .vjs-control-bar
  .vjs-playback-rate
  .vjs-playback-rate-value {
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

.vjs-custom-skin
  > .video-js
  .vjs-control-bar
  .vjs-resolution-button
  .vjs-resolution-button-label {
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
