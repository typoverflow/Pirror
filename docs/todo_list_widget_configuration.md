
  + 和风天气API Key。本项目使用和风天气的API提供实时天气和天气预报。为此，你需要在[和风天气](https://dev.qweather.com/)注册并获取API密钥。同时，你还需要认证成为个人开发者，才可获取天气预报的API权限。获取后，填写在下面这个地方即可
    ```yml
    weather: 
        API_key:                    # 填写和风天气的API Key
    ```
  + Microsoft To Do Client ID and secret. 目前，对open API提供良好支持的代办清单APP仅有微软To Do应用，因此本项目目前仅支持Microsoft To Do作为代办事项组件的“provider”。由于Microsoft To Do使用Oauth2认证，因此你需要进行如下操作
    + **在Azure portal注册项目**：打开[https://go.microsoft.com/fwlink/?linkid=2083908](https://go.microsoft.com/fwlink/?linkid=2083908)，登录你的微软账户，点击画面中的“New registration”
      ![](img/2021-06-12-14-07-07.png)
      然后名字一栏填入“Pirror”，在“Redirect URI”填入“https://www.baidu.com”
      ![](img/2021-06-12-14-12-10.png)
    + **开启项目权限**：在左侧边栏点击“API permissions”，选择“Add a permission”。
      ![](img/2021-06-12-14-12-43.png)
      在弹出的页面中选择“Microsoft Graph”
      ![](img/2021-06-12-14-15-05.png)
      在搜索框中搜索“offline_access”，勾选，并点击下方的“Add permissions”
      ![](img/2021-06-12-14-16-14.png)
      在搜索框中搜索“Tasks.readwrite”，勾选，并点击下方的“Add permissions”
      ![](img/2021-06-12-14-17-12.png)
      在左侧边栏点击Overview界面，记录下你的“Application (client)ID ”
      ![](img/2021-06-12-14-19-37.png)
      然后找到右侧的“Client credentials”，点击“Add a certificate or secret”
      ![](img/2021-06-12-14-23-31.png)
      在页面中点击“New client secret”，然后在右侧的窗口中添加一个secret
      ![](img/2021-06-12-14-24-59.png)
      记录下secret的值
      ![](img/2021-06-12-14-25-38.png)
    + **填写config.yml**：在`config.yml`中，将刚刚记录的“Application (client) ID”的值和“secret value”分别填入“Microsoft”栏目下的“client id”和“client secret”，完成！
      ```bash
      microsoft: 
        client_id:                # 填写client id
        client_secret:            # 填写client secret
      ```