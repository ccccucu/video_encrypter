import service from '@/utils/request'

//获取列表信息（GET）
export const queryLoginLogs = (params) => {
  return service.post('/api/login_log', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteLoginLog = (id) => {
  return service.delete(`/api/login_log/${id}`)
}

//更细单条信息
export const updateLoginLog = (id, params) => {
  return service.put(`/api/login_log/${id}`, params)
}

//获取单条信息
export const getLoginLog = (id) => {
  return service.get(`/api/login_log/${id}`)
}

//新增一条数据（POST）
export const createLoginLog = (params) => {
  return service.post('/api/login_log', params)
}
