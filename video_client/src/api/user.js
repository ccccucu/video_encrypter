import axios from '@/utils/request'

export function login(data) {
  let d = {'type':'admin', 'password':'admin'}
  return axios({
    url: '/api/login',
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
