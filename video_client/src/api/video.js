import axios from '@/utils/request'

export function videoDownload(videoId) {
    return axios({
      url: '/api/videos/download/:id',
      method: 'get',
      data: {id: videoId}
    })
  }
