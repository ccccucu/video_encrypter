import service from '@/utils/request'

//登录并获取token
export function login(data) {
  return service({
    url: '/api/login', //后端的jwt已经接管登录api ，管理员 用户统一登录接口 ‘/login’
    method: 'post',
    data: data
  })
}

//获得当前用户信息，by token，token在http HEAD种
export function getInfo(token) {
  return service({
    url: '/api/current_user',
    method: 'get',
  })
}

//登出
export function logout() {
  return service({
    url: '/user/logout',
    method: 'get'
  })
}
