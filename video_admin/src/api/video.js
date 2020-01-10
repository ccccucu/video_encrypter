import axios from '@/utils/request'

//获取列表信息（GET）
export const queryVideos = (params) => {
  return axios.post('/api/videos', { _method: 'GET', _args: params })
}

//删除单条信息
export const deleteVideo = (id) => {
  return axios.delete(`/api/videos/${id}`)
}

//更细单条信息
export const updateVideo = (id, params) => {
  return axios.put(`/api/videos/${id}`, params)
}

//获取单条信息
export const getVideo = (id) => {
  return axios.get(`/api/videos/${id}`)
}

//新增一条数据（POST）
export const createVideo = (params) => {
  return axios.post('/api/videos', params)
}


export const getVideoThumbPath = (file) => {
  return `/thumb/${file}`
}