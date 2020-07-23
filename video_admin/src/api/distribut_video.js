import service from '@/utils/request'

//获取列表信息（GET）
export const queryDistributVideos = (params) => {
  return service.post('/api/distribut_videos', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteDistributVideo = (id) => {
  return service.delete(`/api/distribut_videos/${id}`)
}

//更细单条信息
export const updateDistributVideo = (id, params) => {
  return service.put(`/api/distribut_videos/${id}`, params)
}

//获取单条信息
export const getDistributVideo = (id) => {
  return service.get(`/api/distribut_videos/${id}`)
}

//新增一条数据（POST）
export const createDistributVideo = (params) => {
  return service.post('/api/distribut_videos', params)
}
