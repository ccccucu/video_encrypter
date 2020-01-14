# video_encrypter

## video_admin 

视频分发管理终端 

```
yarn 
yarn run serve
```

## video_back 
视频分发服务器软件

## video_client

视频客户端 

```
yarn 
yarn run electron:serve
```

基于 electron 


## video_sdk 

* python的加水印客户端
* python 封装后的加密解密的客户端
* 提供 json-rpc 调用


* 基于浏览器native的跨平台客户端开发技术
* 基于协程的高并发服务器开发技术
* 基于mvvc的前端用户界面开发技术
* 基于本地rpc的跨语言调用技术




# 部署教程

## 依赖 根据系统版本 下好

* **docker** 这个一定要
* gcc
* **mysql 5.7**
* redis
* **nginx**

## 简单版本

1. 安装 mysql 和 docker

```
dpkg -i mysql_xxxxx
```


2. docker image file

```
docker import 导入镜像
```

启动

```
docker run  -p 8082:8082
```

配置 nginx:

修改 nginx 配置文件 然后重启nginx

```
nginx -s reload 
```








