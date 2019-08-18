<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  created() {
          setInterval(()=>{
        Rpc.Ping(path).catch((err)=>{
          this.player.stop()
          this.$message.error('本地服务错误，请检查系统状态');
        })
      }, 2630)
  },

}
</script>
