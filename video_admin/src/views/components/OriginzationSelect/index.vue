<template>
    <div>
        <el-cascader
        v-model="organization_id"
        :props="cascader_props"
        @change="handleChange">
        </el-cascader>
    </div>
</template>

<script>
  //mixin
  //视频接口
  import { queryOrganizations, deleteOrganization, updateOrganization, getOrganization, createOrganization } from '@/api/organization'

  export default {
    name: 'OrgaizationSelect',
    props: {
        value: undefined
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
              lazyLoad: (node, resolve) => {
                  const {level} = node
                  let father_organization_id = 0;
                  if (level !== 0) {
                    father_organization_id = node.data.id
                  }
                  debugger
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
