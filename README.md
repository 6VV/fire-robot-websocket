# 机器人控制，WebSocket

## script  

    此文件夹下放置为实际运行代码
    负责机器人及客户端间的数据转发、存储

## 执行  

    python main.py

## mock  

    此文件夹下放置的为模拟数据代码
    负责模拟机器人及客户端的数据

## 执行
    python main.py

## 端口信息

### 本地=》服务器：  

    info:20000  
    panorama-video: 20002  
    fire-branch-video:20003
    map:20004

### 服务器=》本地：  

    info:20001

### 服务器=》客户端：  

    推送数据到客户端

#### 名称及端口

    info:5701

#### 1、水炮视频

    fire-branch-video:5679

#### 2、全景视频  

    panorama-video:5680  

#### 3、SLAM地图

    map:5681  

### 客户端=>服务器：  

    获取客户端传来的数据

#### 名称及端口：  

    info:5700

#### 1、底盘控制

#### 2、火炮控制
