<template>
  <div class="app-container">


    <div class="app-container">
      <!-- <div>模板列表</div> -->
      <br>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" v-model="query">
          <el-form-item label="视频标题：">
            <el-input v-model="query._like_title" placeholder="请输入视频标题"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button plain @click="onReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-col>


      <el-table
        :data="data"
        v-loading="tableLoading"
        @sort-change="onSort">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="分发单位">
                <span>{{ props.row.name }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          prop="id"
          label="编号"
          sortable
          width="80">
        </el-table-column>
        <el-table-column
          prop="title"
          label="标题"
          sortable
          width="180">
        </el-table-column>
        <el-table-column
          prop="upload_unit"
          label="上传单位"
          sortable>
        </el-table-column>
        <el-table-column
          prop="created_by"
          label="上传管理员"
          sortable>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="上传时间"
          sortable>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
            size="mini"
            type="primary">查看</el-button>
            <el-button
              size="mini"
              type="primary">播放</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-col :span="24" class="toolbar">
        <el-pagination
          :current-page="pages._page"
          :page-size="pages._per_page"
          layout="total, prev, pager, next"
          :total="total"
          style="float:right;">
        </el-pagination>
      </el-col>

    </div>
  </div>
</template>

<script>
  //mixin
  import commonTable from '@/mixins/table'
  //视频接口
  import { queryVideos, deleteVideo, updateVideo, getVideo, createVideo } from '@/api/video'

  export default {
    mixins: [commonTable],
    data() {
      return {
        //配置minxin种curd api方法：
        newMethod: createVideo,
        deleteMethod: deleteVideo,
        updateMethod: updateVideo,
        getMethod: getVideo,
        queryMethod: queryVideos,

        //配置mixin query
        query: {  //条件查询 dict  //api查询条件dict
          _like_title: undefined
        },
        //配置mixin query
        resource_name: 'video',

        // tableData: [{
        //   id: 1,
        //   title: '测试视频',
        //   upload_unit: '测试单位',
        //   created_by: '测试管理员',
        //   created_at: '2019-01-01 12:00:00'
        // }]
        data: []  //视频列表



      }
    },
    created() {
    },
    methods: {
      //Rewrite minxin onSearch() 查询
      // onSearch() {
      // },
      //Rewrite minxin onReset()  查询条件重置
      onReset() {
        this.query = {  //条件查询 dict
          _like_title: undefined
        }
        this.order = { _order_by: 'id', _desc: true } //order 在
        this.pages._page = 1
        this.fetchData()
      },

      //获取视频列表信息
      setVideos(query) {
        queryVideos({_page:1,_per_page:30,_like_title:query}).then(res => {
          this.data = res.data.videos;
        })
      },

    },
    mounted() {
      this.setVideos("")
    }

  }
</script>
