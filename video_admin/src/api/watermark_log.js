import service from '@/utils/request'

//获取列表信息（GET）
export const queryWatermarkLogs = (params) => {
  return service.post('/api/watermark_logs', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteWatermarkLog = (id) => {
  return service.delete(`/api/watermark_logs/${id}`)
}

//更细单条信息
export const updateWatermarkLog = (id, params) => {
  return service.put(`/api/watermark_logs/${id}`, params)
}

//获取单条信息
export const getWatermarkLog = (id) => {
  return service.get(`/api/watermark_logs/${id}`)
}

//新增一条数据（POST）
export const createWatermarkLog = (params) => {
  return service.post('/api/watermark_logs', params)
}
