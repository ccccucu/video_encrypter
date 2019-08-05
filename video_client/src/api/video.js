import {ipcMain} from 'electron'
import axios from '@/utils/request'
import httpAdapter from '@/utils/http'

const BASE_URL = 'http://47.104.148.221:8082'

export function videoDownload(videoId) {
    return axios({
      url: `${BASE_URL}/videos/download/${videoId}`,
      method: 'get',
      responseType: 'stream',
      adapter:httpAdapter
    })
  }

  export function queryVideos (args)  {
    return axios.post('/api/videos',
      {"_method": "GET", "_args": args})
  }


