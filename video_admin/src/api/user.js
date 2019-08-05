import axios from '@/utils/request'

export function login(data) {
  let d = {'type':'admin', 'password':'123456'}
  return axios({
    url: '/api/login', //后端的jwt已经接管登录api ，管理员 用户统一登录接口 ‘/login’
    method: 'post',
    data: d
  })
}

export function getInfo(token) {
  return axios({
    url: '/api/current_user',
    method: 'get',
  })
}

export function logout() {
  return axios({
    url: '/user/logout',
    method: 'post'
  })
}
