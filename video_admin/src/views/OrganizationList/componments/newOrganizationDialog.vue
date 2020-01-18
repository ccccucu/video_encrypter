<template>
  <el-dialog title="添加模板" :visible="visible" @close="handleCancel">
    <el-form :model="data" ref="data" :rules="uploadRules" label-width="80px">
      <el-form-item label="编号" prop="account">
        <el-input v-model="data.account" ref="account"></el-input>
      </el-form-item>

      <el-form-item label="名称" prop="name">
        <el-input v-model="data.name" ref="name"></el-input>
      </el-form-item>

      <el-form-item label="负责人姓名" prop="responsible_name">
        <el-input v-model="data.responsible_name" ref="responsible_name"></el-input>
      </el-form-item>

      <el-form-item label="负责人电话" prop="responsible_phone">
        <el-input v-model="data.responsible_phone" ref="responsible_phone"></el-input>
      </el-form-item>

      <el-form-item label="轮班电话" prop="organization_duty_phone">
        <el-input v-model="data.organization_duty_phone" ref="organization_duty_phone"></el-input>
      </el-form-item>

      <el-form-item label="上级组织">
        <OriginzationSelect v-model="data.organization_id" placeholder="请输入管理员姓名"></OriginzationSelect>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { isEmpty } from "@/utils/validate";
import commonNewDialog from "@/mixins/new_dialog";
import { queryOrganizations } from "@/api/organization";
 import OriginzationSelect from '@/views/components/OriginzationSelect'

export default {
  mixins: [commonNewDialog],
  components :{OriginzationSelect},
  data() {
    return {
      data: {
        account: "",
        name: "",
        responsible_name: "",
        responsible_phone: "",
        organization_duty_phone: "",
        father_organization_id: undefined
      },
      uploadRules: {
        account: [
          { required: true, trigger: "blur", message: "编号 不能为空" }
        ],
          name: [
          { required: true, trigger: "blur", message: " 单位名称 不能为空" }
        ],
        responsible_name: [{ required: true, trigger: "blur", message: "负责姓名 不能为空" }],
        responsible_phone: [
          { required: true, trigger: "blur", message: "负责人电话 不能为空" }
        ],
        organization_duty_phone: [{ required: true, trigger: "blur", message: "轮班电话 不能为空" }],
        father_organization_id: [
          { required: true, trigger: "blur", message: "父组织 不能为空" }
        ]
      },
    };
  },
  methods: {

    handleSubmit() {
      this.$refs.data.validate(valid => {
        if (valid) {
          this.$emit("onOK", this.data);
        }
      });
    }
  },
  mounted() {
  }
};
</script>
