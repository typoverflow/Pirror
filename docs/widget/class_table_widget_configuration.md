# 课程表widget配置
+ `update_cycle`: **课程表组件更新信息的间隔**（分钟），保持默认配置1440即可。
+ `begin_date`: **学期开始的日期**，形式为`"YYYY-MM-DD"`
+ `table`: **课程表的具体内容**。其中设有`Monday, Tuesday`子模块，用于配置每一天内的课程内容。
  + 对于类似`Monday`的子模块，它需要的是一个List。List中的每一项代表一项课程，具有5个属性，分别是课程名`name`，开始的周数`start`，结束的周数`end`，教室`room`，时间`range`。

---
一个可供参考的样例如下
```yml
class_table:
  update_cycle: 1440
  begin_date: "2021-03-01"
  table: 
    Monday:
      - name: 博弈论及其应用
        start: 2 
        end: 17
        room: 仙I-108
        range: 9-10

    Tuesday:
      - name: 计算方法
        start: 2
        end: 17
        room: 仙I-108
        range: 5-6
    Wednesday:
      - name: 矩阵计算
        start: 2
        end: 17
        room: 仙II-103
        range: 5-6
      - name: 博弈论及其应用
        start: 2 
        end: 17
        room: 仙I-108
        range: 9-10
      - name: 模式识别与CV
        start: 2
        end: 17
        room: 仙II-304
        range: 3-4
      - name: 计算方法
        start: 2
        end: 17
        room: 仙I-108
        range: 5-6
    Thursday:
      - name: 矩阵计算
        start: 2
        end: 17
        room: 仙II-103
        range: 5-6
      - name: 博弈论及其应用
        start: 2 
        end: 17
        room: 仙I-108
        range: 9-10
      - name: 模式识别与CV
        start: 2
        end: 17
        room: 仙II-304
        range: 3-4
      - name: 计算方法
        start: 2
        end: 17
        room: 仙I-108
        range: 5-6
    Friday: 
    Saturday: 
      - name: 矩阵计算
        start: 2
        end: 17
        room: 仙II-103
        range: 5-6
      - name: 博弈论及其应用
        start: 2 
        end: 17
        room: 仙I-108
        range: 9-10
      - name: 模式识别与CV
        start: 2
        end: 17
        room: 仙II-304
        range: 3-4
```

以星期六为例，代表星期六当天有矩阵计算、博弈论及其应用、模式识别与CV、三门课程，分别是当天的第5-6、9-10、3-4门课。