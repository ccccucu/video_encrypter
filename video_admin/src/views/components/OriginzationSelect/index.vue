<template>
        <el-cascader
        v-model="organization_id"
        :props="cascader_props"
        @change="handleChange">
        </el-cascader>
</template>

<script>
  //mixin
  //视频接口
  import { queryOrganizations, deleteOrganization, updateOrganization, getOrganization, createOrganization } from '@/api/organization'

  export default {
    name: 'OrgaizationSelect',
    props: {
        value: Number,
        multi: {
        type: Boolean,
        required: false,
        default: false
      },
    },
    data() {
      return {
          organization_id: undefined,
          cascader_props: { 
              expandTrigger: 'hover',  
              checkStrictly: true,
              value: 'id',
              label: 'name',
              lazy: true,
              multiple: this.multi,
              lazyLoad: (node, resolve) => {
                  const {level} = node
                  let father_organization_id = 0;
                  if (level !== 0) {
                    father_organization_id = node.data.id
                  }
                queryOrganizations({
                    'father_organization_id': father_organization_id
                }).then((resp) => {
                    resolve(resp.data.organizations);
                })
              }
            }
      }
    },
    methods: {
        handleChange: function(value) {
            this.$emit('input', this.organization_id)
        }
    }

  }
</script>
