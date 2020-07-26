<template>

    <div class="app-container">
      <!-- <div>模板列表</div> -->
      <h1>视频播放</h1>
      <br>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" v-model="query">
          <el-form-item label="水印标题：">
            <el-input v-model="query._search_watermark" placeholder="水印标题"></el-input>
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
          prop="id"
          label="编号"
          sortable
          width="80">
        </el-table-column>
        <el-table-column
          prop="watermark"
          label="水印"
          sortable
          width="180">
        </el-table-column>
        <el-table-column
          prop="video.title"
          label="视频标题"
          sortable>
        </el-table-column>
        <el-table-column
          prop="organization.name"
          label="单位"
          sortable>
        </el-table-column>
        <el-table-column
          prop="user.name"
          label="用户"
          sortable>
        </el-table-column>
        <el-table-column
          prop="ip"
          label="IP"
          sortable>
        </el-table-column>
        <el-table-column
          prop="time"
          label="时间"
          sortable>
        </el-table-column>

        <!--<el-table-column label="操作">-->
          <!--<template slot-scope="scope">-->
            <!--<el-button-->
              <!--size="mini"-->
              <!--type="primary">查看</el-button>-->
          <!--</template>-->
        <!--</el-table-column>-->

      </el-table>

      <el-col :span="24" class="toolbar">
        <el-pagination
          @current-change="onPageChange"
          :current-page="pages._page"
          :page-size="pages._per_page"
          layout="total, prev, pager, next"
          :total="total"
          style="float:right;">
        </el-pagination>
      </el-col>

    </div>
</template>

<script>
  //mixin
  import commonTable from '@/mixins/table'
  //水印接口
  import { queryWatermarkLogs, deleteWatermarkLog, updateWatermarkLog, getWatermarkLog, createWatermarkLog } from '@/api/watermark_log'
  export default {
    mixins: [commonTable],
    data() {
      return {

        //配置minxin种curd api方法：
        newMethod: createWatermarkLog,
        deleteMethod: deleteWatermarkLog,
        updateMethod: updateWatermarkLog,
        getMethod: getWatermarkLog,
        queryMethod: queryWatermarkLogs,

        //配置resource_name
        resource_name: 'watermark_log',

        //配置mixin query
        query: {  //条件查询 dict  //api查询条件dict
          _search_watermark: undefined,
        },

        data: [],  //列表

      }
    },
    created() {
    },
    methods: {}
  }
</script>
