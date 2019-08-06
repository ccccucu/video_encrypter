<template>
  <el-dialog title="分配视频" :visible="visible" @close="handleCancel">
    <el-form :model="data" label-width="80px" ref="templateForm">

      <el-form-item label="选择部门">
        <el-select v-model="data.organization_id"
                   clearable
                   placeholder="请选择">
          <el-option
            v-for="organization in organizations"
            :key="organization.id"
            :label="organization.name"
            :value="organization.id">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
  import { queryOrganizations }  from '@/api/organization'
  import { queryDistributVideos, createDistributVideo } from '@/api/distribut_video'

export default {
  props: {
    video_id: Number,
    visible: Boolean,
    onCancel: Function,
    onOK: Function
  },
  data() {
    return {
      data: {
        video_id: this.video_id,
        video_uuid: "",
        video_title:'测试video_id',
        organization_id: undefined,
        organization_account: "**部门"
      },

      organizations: [],  //部门列表

    }
  },
  methods: {
    handleCancel() {
      this.$emit('onCancel');
    },
    handleSubmit() {
      this.$emit('onOK', this.data);
    },
    //获取部门信息
    setOrganizations(){
      queryOrganizations({}).then(res => {
        this.organizations = res.data.organizations
      })
    },

  },
  created(){

  },
  mounted() {
    this.setOrganizations()

  }

}
</script>
