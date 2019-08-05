const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,    //用户使用设备？？？
  token: state => state.user.token,      //token
  avatar: state => state.user.avatar,  //头像
  name: state => state.user.name,   //昵称或姓名
  roles: state => state.user.roles,   //用户角色
  permission_routes: state => state.permission.routes
}
export default getters
