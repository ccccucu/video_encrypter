<template>
  <div class="dashboard-container">
    <!--<div class="dashboard-text">name:{{ name }}</div>-->
    <div class="dashboard-text">
      <!--roles:-->
      <!--<span v-for="role in roles" :key="role">{{ role }}</span>-->
      <el-form class="form" inline>
        <template v-for="item in permission_routes">
          <div v-if="item.children && item.meta">
            <el-col :span="24">{{item.meta.title}}</el-col>
            <div v-for="c in item.children" :key="c.path">
              <el-form-item class="manage-card-item" v-if="item.children" :key="item.path">
                <el-card
                  class="manage-card"
                  @click.native="handleSelect(c.name)"
                  :key="`menu-${item.name}`"
                >
                  <el-row>
                    <el-col :span="2"></el-col>
                    <el-col style="margin-left: 10px" :span="10">
                      <i class="iconfont" :class="c.meta.icon"></i>
                    </el-col>
                    <el-col :span="12">{{c.meta.title}}</el-col>
                  </el-row>
                </el-card>
              </el-form-item>
            </div>
          </div>
        </template>
      </el-form>
    </div>
  </div>
</template>

<script lang="js">
  import ElCard from "element-ui/packages/card/src/main";
  import { mapGetters } from 'vuex'

  export default {
    name: "",
    components: {ElCard},
    data() {
      return {
        not_show: ['/404', '*', 'login']
      }
    },
    methods: {
      handleSelect(name) {
        this.$router.push({name: name});
      }
    },
    computed: {
      ...mapGetters([
      'permission_routes',
    ]),
      rtouer () {
        return  this.$router
      }
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.iconfont {
  font-family: "iconfont" !important;
  font-size: 28px;
  width: 40px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.ivu-form-item-content {
  height: 100%;
}

.manage-card {
  cursor: pointer;
  height: 100%;
  width: 100%;
}

.form {
  /*margin: 40px 20px 0 40px;*/
}
</style>

<style lang="scss">
.manage-card-item {
  width: 25%;
  min-width: 217px;
  height: 100px;
  margin-right: 50px;

  .el-form-item__content {
    width: 100%;
  }
}
</style>
