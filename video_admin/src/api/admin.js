import axios from '@/utils/request'

//获取列表信息（GET）
export const queryAdmins = (params) => {
  return axios.post('/api/admins', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteAdmin = (id) => {
  return axios.delete(`/api/admins/${id}`)
}

//更细单条信息
export const updateAdmin = (id, params) => {
  return axios.put(`/api/admins/${id}`, params)
}

//获取单条信息
export const getAdmin = (id) => {
  return axios.get(`/api/admins/${id}`)
}

//新增一条数据（POST）
export const createAdmin = (params) => {
  return axios.post('/api/admins', params)
}
