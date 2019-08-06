<template>
  <el-dialog title="分配视频" :visible="visible" @close="handleCancel">
    <el-form :model="data" label-width="80px" ref="templateForm">

      <el-form-item label="选择部门">
        <el-select v-model="query.organization_id"
                   filterable
                   clearable
                   remote
                   :remote-method="setOrganizations"
                   placeholder="请选择">
          <el-option
            v-for="video in videos"
            :key="user.id"
            :label="user.title"
            :value="user.uuid">
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
import commonNewDialog from '@/mixins/new_dialog'

import queryOrganizations from '@/api/organization'
import queryVideos from '@/api/video'

export default {
  mixins: [commonNewDialog],
  props: {
    video_uuid: String
  },
  data() {
    return {
      data: {
        video_uuid: this.video_uuid,
        video_title:'',
        organization_id:'',
        organization_account:''
      },

      query: {},

      videos: [], //视频列表
      organizations: [],  //部门列表


    }
  },
  methods: {
    //获取视频信息
    // setVideos(query){
    //   queryVideos({_order_by: 'create_at', _desc: true}).then(res => {
    //       this.videos = res.data.videos
    //   })
    // },
    //获取部门信息
    // setOrganizations(query){
    //   queryOrganizations({_order_by: 'create_at', _desc: true}).then(res => {
    //     this.organizations = res.data.organizations
    //   })
    // },
    setOrganizations(query){}


  },
  mounted() {
    // this.setVideos("")
    this.setOrganizations("")
  }



}
</script>
