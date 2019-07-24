<template>
  <div class="app-container">
    <!-- <div>模板列表</div> -->
    <br>
    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline="true" v-model="query">
        <el-form-item label="昵称">
          <el-input v-model="query._like_nick_name" placeholder="昵称"></el-input>
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
      :default-sort="{prop: 'id', order: 'descending'}"
      @sort-change="onSort">
      <el-table-column
        prop="nick_name"
        label="昵称"
        width="220">
      </el-table-column>
      <el-table-column
        prop="avatar_url"
        label="头像"
        width="220">
        <template slot-scope="scope">
          <img :src="scope.row.avatar_url" height="40" width="40"/>
        </template>
      </el-table-column>
      <el-table-column
        prop="openid"
        label="openid">
      </el-table-column>
      <el-table-column
        prop="created_at"
        label="创建时间"
        width="220">
      </el-table-column>
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

    <EditorDialog
      :data="selected_data"
      :visible="updateDialogShow"
      @onOK="onUpdateOK"
      @onCancel="onUpdateCancel">
    </EditorDialog>

    <CreatorDialog
      :visible="newDialogShow"
      @onOK="onNewOK"
      @onCancel="onNewCancel">
    </CreatorDialog>

  </div>
</template>
<script>
  import commonTable from '@/mixins/table'
  import {queryWxUsers, deleteWxUsers, updateWxUsers, getWxUsers, createWxUsers} from '@/api/wx_users'
  import EditorDialog from './components/updateDialog.vue'
  import CreatorDialog from './components/newDialog.vue'

  export default {
    name: 'UserTable',
    components: {EditorDialog, CreatorDialog},
    mixins: [commonTable],
    data() {
      return {
        resource_name: 'user',
        newMethod: createWxUsers,
        deleteMethod: deleteWxUsers,
        updateMethod: updateWxUsers,
        getMethod: getWxUsers,
        queryMethod: queryWxUsers,
        query: {
          _like_nick_name: undefined
        }
      }
    },
    methods: {}
  }
</script>
<style scoped>
  .toolbar {
    background: #f2f2f2;
    padding: 10px;
    margin: 10px 0px;
  }

  .toolbar .el-form-item {
    margin-bottom: 10px;
  }
</style>

