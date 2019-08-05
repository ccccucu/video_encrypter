import axios from '@/utils/request'

//获取列表信息（GET）
export const queryDistributVideos = (params) => {
  return axios.post('/api/distribut_videos', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteDistributVideo = (id) => {
  return axios.delete(`/api/distribut_videos/${id}`)
}

//更细单条信息
export const updateDistributVideo = (id, params) => {
  return axios.put(`/api/distribut_videos/${id}`, params)
}

//获取单条信息
export const getDistributVideo = (id) => {
  return axios.get(`/api/distribut_videos/${id}`)
}

//新增一条数据（POST）
export const createDistributVideo = (params) => {
  return axios.post('/api/distribut_videos', params)
}
