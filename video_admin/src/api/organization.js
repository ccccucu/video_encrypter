import service from '@/utils/request'

//获取列表信息（GET）
export const queryOrganizations = (params) => {
  return service.post('/api/organizations', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteOrganization = (id) => {
  return service.delete(`/api/organizations/${id}`)
}

//更细单条信息
export const updateOrganization = (id, params) => {
  return service.put(`/api/organizations/${id}`, params)
}

//获取单条信息
export const getOrganization = (id) => {
  return service.get(`/api/organizations/${id}`)
}

//新增一条数据（POST）
export const createOrganization = (params) => {
  return service.post('/api/organizations', params)
}
