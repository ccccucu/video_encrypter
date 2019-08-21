<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
  import { removeToken } from '@/utils/auth'
export default {

  name: 'App',
  mounted(){
    // 关闭浏览器窗口的时候清空浏览器缓存在localStorage的数据
    window.onbeforeunload = function (e) {
      var storage = window.localStorage;
      storage.clear()
      removeToken()
    }
  },

}
</script>
