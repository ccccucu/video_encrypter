import service from '@/utils/request'

//获取列表信息（GET）
export const queryDownloadLogs = (params) => {
  return service.post('/api/download_logs', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteDownloadLog = (id) => {
  return service.delete(`/api/download_logs/${id}`)
}

//更细单条信息
export const updateDownloadLog = (id, params) => {
  return service.put(`/api/download_logs/${id}`, params)
}

//获取单条信息
export const getDownloadLog = (id) => {
  return service.get(`/api/download_logs/${id}`)
}

//新增一条数据（POST）
export const createDownloadLog = (params) => {
  return service.post('/api/download_logs', params)
}
