<template>
  <div class="app-container">
    <OrganizationTable :father_organization_id="1"></OrganizationTable>
  </div>
</template>

<script>
  import OrganizationTable from './componments/OrganizationTable'
  export default {
    components: {OrganizationTable},
    data() {
      return {
      }
    },
    created() {
    },
    methods: {
      //Rewrite minxin onReset()  查询条件重置
    },
    mounted() {

    }

  }
</script>
