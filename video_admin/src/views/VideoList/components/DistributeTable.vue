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
          prop="organization_account"
          label="分发单位"
          width="200">
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="分配时间"
          width="160">
        </el-table-column>
        <el-table-column
          prop="created_by"
          label="分配者"
          width="120">
        </el-table-column>

        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="warning"
              @click="onDeleteClick(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-button
        size="mini"
        type="primary"
        @click="onNewClick">分配视频</el-button>

      <CreatorDialog
        :visible="newDialogShow"
        :video_id = "video_id"
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
      video_id: Number
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
        query: { video_id: this.video_id } //应该是video_id 但是后端未更新   { id: this.video_id }
      }
    },
    methods: {

    },

    mounted(){
      window.vue = this
    }
  }
</script>

<style>

</style>
