/* eslint-disable prefer-const */
import axios from '@/utils/request'

export function login(data) {
  return axios({
    url: '/api/login',
    method: 'post',
    data: data
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

