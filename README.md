# WebChat聊天室

## 依赖环境

1. python 2.7.18(请确保使用正确的python版本,因为tornado-redis与高版本python可能出现兼容性问题)
2. tornado
3. redis-server
4. sqlite3

## 启动WebChat服务

```
$ redis-server (开启redis服务)
$ python init_sqlite.py (第一次使用请运行,初始化数据库)
$ python server.py (启动WebChat服务)
在浏览器中访问 localhost:8200 即可开始使用WebChat
```
## 项目说明

### 前端

利用semantic-ui的ccs文件,进行页面美化(https://semantic-ui.com/)
使用基于ajax的longpolling向后端传送数据

### 后端

采用redis的sub/pub机制获取信息
利用sqlite3作为数据库

## 项目功能

1. 用户注册/登陆,有基本的密码验证机制
2. 支持修改密码
3. 支持通过搜索添加好友
4. 支持通过在好友中搜索,并邀请好友进入聊天室

## 场景展示
注册账号
![alt 注册](pic/Screen%20Shot%202022-05-11%20at%2003.01.25%20(2).png)
添加好友
![alt 添加好友](pic/Screen%20Shot%202022-05-11%20at%2003.05.50.png)
开始私聊
![alt 私聊](pic/Screen%20Shot%202022-05-11%20at%2003.22.54.png)
创建讨论室
![alt 讨论室](pic/Screen%20Shot%202022-05-11%20at%2003.23.33.png)
修改密码
![alt 修改密码](pic/Screen%20Shot%202022-05-11%20at%2003.24.31.png)