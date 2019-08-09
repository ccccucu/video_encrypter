import { mapState, mapMutations} from 'vuex'

export default {
  computed:{
    ...mapState({
      userInfo:  state => state.user.info,
      roles: state => state.user.roles
    }),
  },
}
