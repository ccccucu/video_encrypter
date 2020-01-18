<template>
    <div >
      <!-- <div>模板列表</div> -->

      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" v-model="query">
          <!-- <el-form-item label="管理员姓名：">
            <el-input v-model="query._like_name" placeholder="请输入管理员姓名"></el-input>
          </el-form-item> -->

          <el-form-item label="根组织">
            <OriginzationSelect v-model="query.father_organization_id" placeholder="请输入管理员姓名"></OriginzationSelect>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="onSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button plain @click="onReset">重置</el-button>
          </el-form-item>

          <el-form-item style="float: right">
            <el-button type="success"  @click="onNewClick">添加用户</el-button>
          </el-form-item>
        </el-form>
      </el-col>


      <el-table
        :data="data"
        v-loading="tableLoading"
        @sort-change="onSort" 
        type="expand">
        <!-- <el-table-column type="expand">
          <template slot-scope="scope"> 
            <el-card class="box-card">
            <OrgaizationTable :father_organization_id="scope.row.id"> 
            </OrgaizationTable>
            </el-card>
          </template>
        </el-table-column> -->
        <el-table-column
          prop="id"
          label="id"
          sortable
          width="80">
        </el-table-column>
        <el-table-column
          prop="account"
          label="编号"
          sortable
          width="180">
        </el-table-column>
        <el-table-column
          prop="name"
          label="姓名"
          sortable>
        </el-table-column>
        <el-table-column
          prop="responsible_name"
          label="单位负责人姓名"
          sortable>
        </el-table-column>
        <el-table-column
          prop="organization_duty_phone"
          label="单位值班电话"
          sortable>
        </el-table-column>
        <el-table-column
          prop="responsible_phone"
          label="单位负责人电话"
          sortable>
        </el-table-column>
        <el-table-column
          prop="father_organization.name"
          label="上级单位"
          sortable>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
            size="mini"
            type="primary">查看</el-button>
            <el-button
            size="mini"
            type="danger"
            @click="onDeleteClick(scope.$index, scope.row)">删除</el-button>
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

      <CreatorDialog
        :visible="newDialogShow"
        @onOK="onNewOK"
        @onCancel="onNewCancel">
      </CreatorDialog>

    </div>
</template>

<script>
  //mixin
  import commonTable from '@/mixins/table'
  import OriginzationSelect from '@/views/components/OriginzationSelect'
  //视频接口
  import { queryOrganizations, deleteOrganization, updateOrganization, getOrganization, createOrganization } from '@/api/organization'
import CreatorDialog from './newOrganizationDialog.vue'

  export default {
    name: 'OrgaizationTable',
    components: {OriginzationSelect, CreatorDialog},
    mixins: [commonTable],
    props: {
    },
    data() {
      return {
        //配置minxin种curd api方法：
        newMethod: createOrganization,
        deleteMethod: deleteOrganization,
        updateMethod: updateOrganization,
        getMethod: getOrganization,
        queryMethod: queryOrganizations,

        //配置resource_name
        resource_name: 'organization',

        //配置mixin query
        query: {  //条件查询 dict  //api查询条件dict
          _like_name: undefined,
          father_organization_id: undefined,
        },
        data: [],  //视频列表

      }
    },
    methods: {
      //Rewrite minxin onReset()  查询条件重置
      onReset() {
        this.query = {  //条件查询 dict
          _like_name: undefined,
          father_organization_id: undefined
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
