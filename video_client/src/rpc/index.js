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

Rpc.redaLocalFile = function(path){
    //console.log(`${BASE_URL}/api/read_file`)
    return axios.get(`${BASE_URL}/rpc/read_file`, { params: {'path': path} })
}

Rpc.downloadFile = function(path){
    // return axios.get('http://47.104.148.221:8082/videos/download/'+ path)
    return axios.get('http://47.104.148.221:8082/videos/download/'+ path)
}

Rpc.readVideoList = function(){
    return axios.post('http://47.104.148.221:8082/videos', {"_method": "GET", "_args": {}})
    // .then( (response)=> {
    //   console.log(response);
    //   this.tableData = response.data.videos;
    // });
}

export default Rpc;
