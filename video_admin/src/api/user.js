import axios from '@/utils/request'

//获取列表信息（GET）
export const queryUsers = (params) => {
  return axios.post('/api/users', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteUser = (id) => {
  return axios.delete(`/api/users/${id}`)
}

//更细单条信息
export const updateUser = (id, params) => {
  return axios.put(`/api/users/${id}`, params)
}

//获取单条信息
export const getUser = (id) => {
  return axios.get(`/api/users/${id}`)
}

//新增一条数据（POST）
export const createUser = (params) => {
  return axios.post('/api/users', params)
}
