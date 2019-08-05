import axios from '@/utils/request'

//获取列表信息（GET）
export const queryLoginLogs = (params) => {
  return axios.post('/api/login_log', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteLoginLog = (id) => {
  return axios.delete(`/api/login_log/${id}`)
}

//更细单条信息
export const updateLoginLog = (id, params) => {
  return axios.put(`/api/login_log/${id}`, params)
}

//获取单条信息
export const getLoginLog = (id) => {
  return axios.get(`/api/login_log/${id}`)
}

//新增一条数据（POST）
export const createLoginLog = (params) => {
  return axios.post('/api/login_log', params)
}
