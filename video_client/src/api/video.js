import {ipcMain} from 'electron'
import axios from '@/utils/request'
import httpAdapter from '@/utils/http'

const BASE_URL = 'http://0.0.0.0:5005/'

export function videoDownload(videoId) {
    return axios({
      url: `${BASE_URL}/videos/download/${videoId}`,
      method: 'get',
      responseType: 'stream',
      adapter:httpAdapter
    })
  }

  export function queryVideos (args)  {
    return axios.post('/api/videos/distribute',
      {"_method": "GET", "_args": args})
  }


