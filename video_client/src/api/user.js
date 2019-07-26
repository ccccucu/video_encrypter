import axios from '@/utils/request'

var UserApi = {}

UserApi.login =  function login(data) {
  let d = {'type':'admin', 'password':'admin'}
  return axios({
    url: '/api/login',
    method: 'post',
    data: d
  })
}

UserApi.getInfo = function getInfo(token) {
  return axios({
    url: '/api/current_user',
    method: 'get',
  })
}

UserApi.logout =  function logout() {
  return axios({
    url: '/user/logout',
    method: 'post'
  })
}

export default UserApi;