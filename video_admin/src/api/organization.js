import axios from '@/utils/request'

//获取列表信息（GET）
export const queryOrganizations = (params) => {
  return axios.post('/api/organizations', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteOrganization = (id) => {
  return axios.delete(`/api/organizations/${id}`)
}

//更细单条信息
export const updateOrganization = (id, params) => {
  return axios.put(`/api/organizations/${id}`, params)
}

//获取单条信息
export const getOrganization = (id) => {
  return axios.get(`/api/organizations/${id}`)
}

//新增一条数据（POST）
export const createOrganization = (params) => {
  return axios.post('/api/organizations', params)
}
