<template>
  <el-dialog title="添加模板" :visible="visible" @close="handleCancel">
    <el-form :model="data" ref="data" :rules="uploadRules" label-width="80px">
      
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

export default {
  mixins: [commonNewDialog],
  data() {
    return {
      data: {

      },
      uploadRules: {
        uuid: [{ required: true, trigger: "blur", message: "编号 不能为空" }],
        account: [
          { required: true, trigger: "blur", message: "账号 不能为空" }
        ],
        ip: [{ required: true, trigger: "blur", message: "ip 不能为空" }],
        name: [{ required: true, trigger: "blur", message: "姓名 不能为空" }],
        organization_id: [
          { required: true, trigger: "blur", message: "组织 不能为空" }
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
