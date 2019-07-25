<template>

    <div class="app-container">
      <!-- <div>模板列表</div> -->
      <h1>视频播放</h1>
      <br>
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" v-model="query">
          <el-form-item label="视频标题：">
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
        :data="tableData">
        <el-table-column
          prop="id"
          label="编号"
          width="80">
        </el-table-column>
        <el-table-column
          prop="water_mark"
          label="水印"
          width="180">
        </el-table-column>
        <el-table-column
          prop="video"
          label="视频标题">
        </el-table-column>
        <el-table-column
          prop="unit"
          label="单位">
        </el-table-column>
        <el-table-column
          prop="created_by"
          label="用户">
        </el-table-column>
        <el-table-column
          prop="ip"
          label="IP">
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="时间">
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
</template>

<script>

  export default {
    data() {
      return {
        total: 1,
        query: {},
        pages: {
          _per_page:30,
          _page: 1
        },
        tableData: [{
          id: 1,
          water_mark: "xxxx",
          video: '测试视频',
          unit: '测试单位',
          ip: '0.0.0.0',
          created_by: '测试管理员',
          created_at: '2019-01-01 12:00:00'
        }]
      }
    },
    created() {
    },
    methods: {}
  }
</script>
