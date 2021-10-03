# 天气预报widget配置
我们借助「和风天气」提供的API来实现天气预报功能。具体而言，你需要
+ 在[「和风天气开发平台」](https://dev.qweather.com/)注册账户
+ 参考[这个文档](https://dev.qweather.com/help/account/#enroll-developer)，认证成为**个人开发者**
+ 参考[这个文档](https://dev.qweather.com/docs/start/get-key/)，创建应用并获取密钥KEY
+ 完善`config.yml`中和weather widget相关的配置
  + `update_cycle`为widget更新自身信息的周期，推荐保持默认配置
  + `API_key`: 填写上一步中的KEY
  + `location`: 填写你所在的城市名（注意，你所在的城市并不一定具有气象观测站，则可能会导致Pirror出现不可知的错误）
  + `AQI_station`: 空气质量监测点。一座城市中可能有多个空气质量监测点，在这里可以选择需要参考的站点名，你也可以在这里留空，表示随机选择一个站点。

---
一个可以参考的配置如下
```yml
weather: 
  update_cycle: 60
  API_key: ************
  location: 南京
  AQI_station: 
    - 仙林大学城
    - 奥体中心
```