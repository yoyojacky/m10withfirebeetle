# 行空板M10遇到FireBeetle esp32s3 

## 说明
* 开发环境：
树莓派5 + arduino-cli + esp32s3 + Multifunctional Environmental sensor v2.0 

ESP32代码在esp32_weather
M10代码在M10-python-code 

## M10 上传代码方法
1. 连接m10到usb等待启动。
2. 通过mobaXterm开远程连接到10.1.2.3
```bash 
ssh root@10.1.2.3 
```
密码默认：dfrobot
3. 切换目录到 /opt/unihiker/examples/ 
创建一个你的项目目录:
```bash 
mkdir 12-yoyojacky
cd 12-yoyojacky
```
4. 把仓库中m10的代码拷贝进去，根据你实际情况修改ip地址和端口号信息即可。
