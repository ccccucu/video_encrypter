import {ipcMain} from 'electron'
import axios from '@/utils/request'
import httpAdapter from '@/utils/http'
import {SERVER_URL} from './index'

export function videoDownload(videoId) {
    return axios({
      url: `${SERVER_URL}/videos/download/${videoId}`,
      method: 'get',
      responseType: 'stream',
      adapter:httpAdapter
    })
  }

  export function queryVideos (args)  {
    return axios.post(`${SERVER_URL}/videos/distribute`,
      {"_method": "GET", "_args": args})
  }


