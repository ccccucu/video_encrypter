import axios from '@/utils/request'

//获取列表信息（GET）
export const queryWatermarkLogs = (params) => {
  return axios.post('/api/watermark_logs', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteWatermarkLog = (id) => {
  return axios.delete(`/api/watermark_logs/${id}`)
}

//更细单条信息
export const updateWatermarkLog = (id, params) => {
  return axios.put(`/api/watermark_logs/${id}`, params)
}

//获取单条信息
export const getWatermarkLog = (id) => {
  return axios.get(`/api/watermark_logs/${id}`)
}

//新增一条数据（POST）
export const createWatermarkLog = (params) => {
  return axios.post('/api/watermark_logs', params)
}
