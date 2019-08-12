/* eslint-disable prefer-const */
import axios from '@/utils/request'
import {SERVER_URL} from './index'

export function login(data) {
  return axios({
    url: `${SERVER_URL}/login`,
    method: 'post',
    data: data
  })
}

export function getInfo(token) {
  return axios({
    url: `${SERVER_URL}/current_user`,
    method: 'get',
  })
}

export function logout() {
  return axios({
    url: '/user/logout',
    method: 'post'
  })
}

