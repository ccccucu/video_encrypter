import axios from '@/utils/request'

//登录并获取token
export function login(data) {
  let d = {'type':'admin', 'password':'123456'}
  return axios({
    url: '/api/login', //后端的jwt已经接管登录api ，管理员 用户统一登录接口 ‘/login’
    method: 'post',
    data: d
  })
}

//获得当前用户信息，by token，token在http HEAD种
export function getInfo(token) {
  return axios({
    url: '/api/current_user',
    method: 'get',
  })
}

//登出
export function logout() {
  return axios({
    url: '/user/logout',
    method: 'post'
  })
}
