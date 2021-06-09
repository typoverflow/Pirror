import requests
import pandas
import yaml
import json
import pygame
from utils.log import log

class WeatherWidget(object):
    locationID_list = pandas.read_csv("resources/locationID.csv")
    AQI_api = "https://devapi.qweather.com/v7/air/now"
    realtime_api = "https://devapi.qweather.com/v7/weather/now"
    next24h_api = "https://devapi.qweather.com/v7/weather/24h"
    suggestion_api = "https://devapi.qweather.com/v7/indices/1d"

    def __init__(self, config):
        self.location = config.get("location", "南京")
        self.locationID = WeatherWidget.locationID_list[WeatherWidget.locationID_list["城市名称"]==self.location].iloc[0, 0]
        self.AQI_station = config.get("AQI_station", None)
        self.API_key = config.get("API_key", "")

        self.icon_buffer = {}
        self.AQI_info = None
        self.realtime_info = None
        self.next24h_info = None
        self.suggestion_info = None
        self.update_cycle = config.get("update_cycle", 60)
        self.update_count = 0

    def update_AQI(self):
        r = requests.get(WeatherWidget.AQI_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get AQI info.")
        if self.AQI_station is None:
            self.old_AQI_info = self.AQI_info
            self.AQI_info =  [result["station"][0]["aqi"], result["station"][0]["category"]]
            return self.old_AQI_info != self.AQI_info
        for s in result["station"]:
            if s["name"] == self.AQI_station:
                self.old_AQI_info = self.AQI_info
                self.AQI_info = [s["aqi"], s["category"]]
                return self.old_AQI_info != self.AQI_info

    def update_realtime_weather(self):
        r = requests.get(WeatherWidget.realtime_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get realtime weather info.")
        self.old_realtime_info = self.realtime_info
        self.realtime_info = result["now"]
        return self.old_realtime_info != self.realtime_info

    def update_next24h_weather(self):
        def agg_weather_info(hourlys):
            represent = sorted(hourlys, key=lambda x: x["icon"])
            return represent[0]

        r = requests.get(WeatherWidget.next24h_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get next 24h weather info.")
        self.old_next24h_info = self.next24h_info
        self.next24h_info = [agg_weather_info(result["hourly"][4:4+10]), agg_weather_info(result["hourly"][14:])]
        return self.old_next24h_info != self.next24h_info

    def update_suggestion(self):
        r = requests.get(WeatherWidget.suggestion_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
            "type": "1,5"
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get tips for the day.")
        self.old_suggestion_info = self.suggestion_info
        self.suggestion_info =  {
            "运动": result["daily"][0]["category"], 
            "UV指数": result["daily"][1]["category"]
        }
        return self.old_suggestion_info != self.suggestion_info

    def get_icon(self, code, size):
        entry = "./resources/WeatherIcon/color-{}/{}.png".format(code, size)
        if entry in self.icon_buffer:
            return self.icon_buffer.get(entry)
        self.icon_buffer[entry] = pygame.image.load(entry)
        return self.icon_buffer[entry]

    def update_all(self):
        self.update_count += 1
        if self.update_count % self.update_cycle == 0:
            self.update_count = 0
            updated1 = self.update_AQI()
            updated2 = self.update_next24h_weather()
            updated3 = self.update_realtime_weather()
            updated4 = self.update_suggestion()
            return updated1 or updated2 or updated3 or updated4
        else:
            return False
    
    def render(self, screen):
        pass
    

        

if __name__ == "__main__":
    f = open("configs/config.yml")
    w = WeatherWidget(yaml.load(f)["weather"])
    w.get_next24h_weather()