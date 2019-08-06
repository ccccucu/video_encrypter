<template>
    <div class="app-container">
      <el-table
        :data="data"
        v-loading="tableLoading"
        :default-sort="{prop: 'id', order: 'descending'}"
        @sort-change="onSort">
        <el-table-column
          prop="video_uuid"
          label="视频uuid"
          width="100">
        </el-table-column>
        <el-table-column
          prop="video_title"
          label="视频名称"
          width="220">
        </el-table-column>
        <el-table-column
          prop="organization_account"
          label="分发单位"
          width="200">
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="分配时间"
          width="120">
        </el-table-column>
        <el-table-column
          prop="created_by"
          label="分配者"
          width="100">
        </el-table-column>

        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="warning">删除</el-button>
          </template>
        </el-table-column>
      </el-table>


      <CreatorDialog
        :visible="newDialogShow"
        :video_uuid = "video_uuid"
        :video_title = "video_title"
        @onOK="onNewOK"
        @onCancel="onNewCancel">
      </CreatorDialog>


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

<script type="text/javascript">
  import commonTable from '@/mixins/table'
  import {queryDistributVideos, deleteDistributVideo, updateDistributVideo, getDistributVideo, createDistributVideo} from '@/api/distribut_video'
  import CreatorDialog from './components/newDialog.vue'

  export default {
    name: 'video_distribute_table',
    components: { CreatorDialog },
    mixins: [commonTable],
    props: {
      video_uuid: String,
      video_title: String
    },
    data() {
      return {
        resource_name: 'distribut_video',
        newMethod: createDistributVideo,
        deleteMethod: deleteDistributVideo,
        updateMethod: updateDistributVideo,
        getMethod: getDistributVideo,
        queryMethod: queryDistributVideos,

        //查询条件
        query: { uuid: this.video_uuid }
      }
    },
    methods: {

    },

    mounted(){
    }
  }
</script>

<style>

</style>
