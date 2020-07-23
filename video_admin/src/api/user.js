import service from '@/utils/request'

//获取列表信息（GET）
export const queryUsers = (params) => {
  return service.post('/api/users', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteUser = (id) => {
  return service.delete(`/api/users/${id}`)
}

//更细单条信息
export const updateUser = (id, params) => {
  return service.put(`/api/users/${id}`, params)
}

//获取单条信息
export const getUser = (id) => {
  return service.get(`/api/users/${id}`)
}

//新增一条数据（POST）
export const createUser = (params) => {
  return service.post('/api/users', params)
}
