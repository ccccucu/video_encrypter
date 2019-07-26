import axios from '@/utils/request'

const BASE_URL = '0.0.0.0:10086'

export function callRpc(method, params){
    return axios({
        url: `${BASE_URL}/rpc`,
        method: 'post',
        data:  {
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

export default Rpc;