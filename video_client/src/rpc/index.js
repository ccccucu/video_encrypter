/* eslint-disable space-before-blocks */
import axios from '@/utils/request'

const BASE_URL = 'http://0.0.0.0:10086'

export function callRpc(method, params) {
    return axios({
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

Rpc.enWaterMarkByPath = function(path, outpath) {
    return callRpc('EnWaterMakerByPath', {
        'path': path,
        'outpath': outpath
    })
}

Rpc.readLocalFile = function(path){
    //console.log(`${BASE_URL}/api/read_file`)
    return axios.get(`${BASE_URL}/rpc/read_file`, { params: {'path': path} })
}

Rpc.readLocalUrl = function(path){
  return `file://${path}`
}



export default Rpc;
