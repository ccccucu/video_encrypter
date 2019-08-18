/* eslint-disable space-before-blocks */
import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:10086'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 50000000 // request timeout
})


export function callRpc(method, params) {
    return service({
        url: `${BASE_URL}/rpc`,
        method: 'post',
        data: {
            'method': method,
            'jsonrpc': '2.0',
            'params': params,
            'id': 1
        }
    })
}

var Rpc = {}

Rpc.enWaterMarkByPath = function(path,content, outpath) {
    return callRpc('EnWaterMakerByPath', {
        'path': path,
        'content': content,
        'outpath': outpath
    })
}

Rpc.deWaterMarkByPath = function(path) {
  return callRpc('DeWaterMakerByPath', {
    'path': path,
  })
}

Rpc.clientReadVideo = function(path, key, watermark, outpath) {
  return callRpc('ClientReadVideo', {
    'path': path,
    'key': key,
    'watermark': watermark,
    'outpath': outpath
  })
}

Rpc.readVideoFile = function(path){
    //console.log(`${BASE_URL}/api/read_file`)
    return axios.get(`${BASE_URL}/rpc/read_videos`, { params: {'path': path} })
}

Rpc.readLocalUrl = function(path, key){
  return `${BASE_URL}/read_video?path=${path}&key=${key}`
}

Rpc.Ping = function (path) {
  return callRpc('Ping', {
    'path': path
  })
}

export default Rpc;
