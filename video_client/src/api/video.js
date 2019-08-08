import {ipcMain} from 'electron'
import axios from '@/utils/request'
import httpAdapter from '@/utils/http'
import {SERVEER_URL} from './index'

export function videoDownload(videoId) {
    return axios({
      url: `${SERVEER_URL}/videos/download/${videoId}`,
      method: 'get',
      responseType: 'stream',
      adapter:httpAdapter
    })
  }

  export function queryVideos (args)  {
    return axios.post(`${SERVEER_URL}/videos/distribute`,
      {"_method": "GET", "_args": args})
  }


