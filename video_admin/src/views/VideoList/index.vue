<template>
  <div class="app-container">


    <div class="app-container">
      <!-- <div>模板列表</div> -->

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

        <el-table-column
          type="expand"
          label="分发单位"
          width="80">
          <template slot-scope="props">
            <el-card>
              <DistributeTable
                :video_id="props.row.id">
              </DistributeTable>
            </el-card>
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
          prop="upload_organization.name"
          label="上传单位"
          sortable>
        </el-table-column>
        <el-table-column
          prop="upload_admin.name"
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
  import  DistributeTable from './components/DistributeTable'
  //视频接口
  import { queryVideos, deleteVideo, updateVideo, getVideo, createVideo } from '@/api/video'

  export default {
    mixins: [commonTable],
    components :{
      DistributeTable
    },
    data() {
      return {
        //配置minxin种curd api方法：
        newMethod: createVideo,
        deleteMethod: deleteVideo,
        updateMethod: updateVideo,
        getMethod: getVideo,
        queryMethod: queryVideos,

        //配置resource_name
        resource_name: 'video',

        //配置mixin query
        query: {  //条件查询 dict  //api查询条件dict
          _like_title: undefined
        },

        data: [],  //视频列表

      }
    },
    created() {
    },
    methods: {
      //Rewrite minxin onReset()  查询条件重置
      onReset() {
        this.query = {  //条件查询 dict
          _like_title: undefined
        }
        this.order = { _order_by: 'id', _desc: true } //order 在
        this.pages._page = 1
        this.fetchData()
      },

    },
    mounted() {

    }

  }
</script>
