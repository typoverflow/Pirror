import requests
import pandas
import yaml
import json
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

    def get_AQI(self):
        r = requests.get(WeatherWidget.AQI_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get AQI info.")
        if self.AQI_station is None:
            return [result["station"][0]["aqi"], result["station"][0]["category"]]
        for s in result["station"]:
            if s["name"] == self.AQI_station:
                return [s["aqi"], s["category"]]

    def get_realtime_weather(self):
        r = requests.get(Weather.realtime_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get realtime weather info.")
        return result["now"]

    def get_next24h_weather(self):
        def agg_weather_info(hourlys):
            represent = sorted(hourlys, key=lambda x: x["icon"])
            return represent[0]

        r = requests.get(Weather.next24h_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get next 24h weather info.")
        return agg_weather_info(result["hourly"][4:4+10]), agg_weather_info(result["hourly"][14:])

    def get_suggestion(self):
        r = requests.get(Weather.suggestion_api, params={
            "location": self.locationID, 
            "key": self.API_key, 
            "type": "1,5"
        })
        assert r.status_code == 200
        result = json.loads(r.text)
        assert result["code"] == "200"

        log("\33[0;32;1m", "Success", "Get tips for the day.")
        return {
            "运动": result["daily"][0]["category"], 
            "UV指数": result["daily"][1]["category"]
        }


if __name__ == "__main__":
    f = open("configs/config.yml")
    w = WeatherWidget(yaml.load(f)["weather"])
    w.get_suggestion()