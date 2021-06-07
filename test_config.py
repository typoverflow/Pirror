from widget import todo_list, weather

import yaml

f = open("configs/config.yml")
config = yaml.load(f)

t = todo_list.TodoList(config.get("todo_list"))
w = weather.Weather(config.get("weather"))


w.get_AQI()
w.get_next24h_weather()
w.get_realtime_weather()
w.get_suggestion()
t.get_tasks()