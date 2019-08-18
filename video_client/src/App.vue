<template>
  <div id="app">
    <el-alert v-if="loading" type="error" title="失去本地服务的链接, 马上重试"></el-alert>
    <router-view v-loading="loading" />
  </div>
</template>

<script>
import Rpc from "@/rpc/index";
const { ipcRenderer } = require("electron");

export default {
  name: "App",
  data() {
    return {
      ping_sdk: undefined,
      loading: false,
      times: 0
    };
  },
  methods: {
    pingSDK: function() {
      return Rpc.Ping()
        .then(() => {
          this.times = 0;
          this.loading = false;
        })
        .catch(err => {
          this.loading = true;
        });
    }
  },
  created() {
    this.pingSDK();
    this.ping_sdk = setInterval(() => {
      this.times = this.times + 1;
      if (this.times >= 5) {
        ipcRenderer.send("Video.ResetartSDK");
        this.times = 0;
      }
      this.pingSDK();
    }, 5000);
  },

  beforeDestroy() {
    clearInterval(this.ping_sdk);
  }
};
</script>
