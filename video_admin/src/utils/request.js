import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 50000000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation

      //config.headers['X-Token'] = getToken()

      //flask_jwt needs:
      config.headers['Authorization'] = 'Bearer ' + getToken()

    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data
    // if the custom code is not 20000, it is judged as an error.
    if (res.code !== 200) {
      Message({
        message: res.msg || 'error',
        type: 'error',
        duration: 5 * 1000
      })
    } 
    return response
  
  },
  error => {
    if (error.response.status == 500){
      Message({
        message: "服务器错误",
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (error.response.status == 401) {
      Message({
        message: "用户名密码错误",
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (error.response.status == 403) {
      Message({
        message: "用户没有权限",
        type: 'error',
        duration: 5 * 1000
      })
    }
    return Promise.reject(error)
  }
)

export default service
