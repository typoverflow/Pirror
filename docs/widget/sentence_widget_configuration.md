# 格言widget配置
我们借助[「Hitokoto」](https://hitokoto.cn/)获取格言。
+ `update_cycle`: 组件本身重新获取新的格言的周期，推荐保持默认配置。
+ `type`: 格言类型，不同的类型使用空格隔开，注意需要用双引号包裹。
  <img src=img/2021-10-03-17-32-53.png width=300>
+ `max_length`: 太长的句子可能会超出屏幕的显示范围（取决于你的屏幕有多大），使用这个配置项可以限制格言的最长长度。

---
一个可以参考的配置文件如下
```yml
sentence: 
    update_cycle: 30
    type: "d h i"
    max_length: 20
```