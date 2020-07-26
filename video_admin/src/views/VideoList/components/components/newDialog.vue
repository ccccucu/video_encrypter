<template>
  <el-dialog title="分配视频" :visible="visible" @close="handleCancel">
    <el-form :model="data" label-width="80px" ref="templateForm">

      <el-form-item label="选择单位">
          <OriginzationSelect v-model="data.organization_id" :multi="false"></OriginzationSelect>
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
  import OriginzationSelect from '@/views/components/OriginzationSelect'

export default {
  components:{OriginzationSelect},
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
        organization_id: undefined,
        created_by: "管理员"
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
