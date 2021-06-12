import requests
import pandas
import yaml
import json
import pygame

from utils.log import log
from ui.gradient import gradientRect
from ui.text import blit_text_in_middle

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
        self.update_cycle = config.get("update_cycle", 60)*60
        self.last_update = 0

    def update_AQI(self):
        try: 
            r = requests.get(WeatherWidget.AQI_api, params={
                "location": self.locationID, 
                "key": self.API_key, 
            })
            assert r.status_code == 200
            result = json.loads(r.text)
            assert result["code"] == "200"

            log("\33[0;32;1m", "Request", "WeatherWidget - get AQI info successfully.")
            if self.AQI_station is None:
                self.old_AQI_info = self.AQI_info
                self.AQI_info =  [result["station"][0]["aqi"], result["station"][0]["category"]]
                return self.old_AQI_info != self.AQI_info
            for s in result["station"]:
                if s["name"] in self.AQI_station:
                    self.old_AQI_info = self.AQI_info
                    self.AQI_info = [s["aqi"], s["category"]]
                    return self.old_AQI_info != self.AQI_info
        except Exception as e:
            log("\33[0;31;1m", "Error", "WeatherWidget.update_AQI - {}.".format(e))
            return False

    def update_realtime_weather(self):
        try: 
            r = requests.get(WeatherWidget.realtime_api, params={
                "location": self.locationID, 
                "key": self.API_key, 
            })
            assert r.status_code == 200
            result = json.loads(r.text)
            assert result["code"] == "200"

            self.old_realtime_info = self.realtime_info
            self.realtime_info = result["now"]

            log("\33[0;32;1m", "Request", "WeatherWidget - get realtime weather info successfully")
            return self.old_realtime_info != self.realtime_info
        except Exception as e:
            log("\33[0;31;1m", "Error", "WeatherWidget.update_realtime - {}.".format(e))
            return False

    def update_next24h_weather(self):
        def agg_weather_info(hourlys):
            represent = sorted(hourlys, key=lambda x: x["icon"])
            return represent[0]

        try: 
            r = requests.get(WeatherWidget.next24h_api, params={
                "location": self.locationID, 
                "key": self.API_key, 
            })
            assert r.status_code == 200
            result = json.loads(r.text)
            assert result["code"] == "200"

            self.old_next24h_info = self.next24h_info
            self.next24h_info = [agg_weather_info(result["hourly"][4:4+10]), agg_weather_info(result["hourly"][14:])]

            log("\33[0;32;1m", "Request", "WeatherWidget - get next24h weather info successfully")
            return self.old_next24h_info != self.next24h_info
        except Exception as e:
            log("\33[0;31;1m", "Error", "WeatherWidget.update_next24h - {}.".format(e))
            return False

    def update_suggestion(self):
        try: 
            r = requests.get(WeatherWidget.suggestion_api, params={
                "location": self.locationID, 
                "key": self.API_key, 
                "type": "1,5"
            })
            assert r.status_code == 200
            result = json.loads(r.text)
            assert result["code"] == "200"

            self.old_suggestion_info = self.suggestion_info
            self.suggestion_info =  {
                "运动": result["daily"][0]["category"], 
                "UV指数": result["daily"][1]["category"]
            }

            log("\33[0;32;1m", "Request", "WeatherWidget - get suggestions for the day successfully")
            return self.old_suggestion_info != self.suggestion_info
        except Exception as e:
            log("\33[0;31;1m", "Error", "WeatherWidget.update_suggestion - {}.".format(e))
            return False

    def get_icon(self, code, size, mode="color"):
        entry = "./resources/WeatherIcon/{}-{}/{}.png".format(mode, size, code)
        if entry in self.icon_buffer:
            return self.icon_buffer.get(entry)
        self.icon_buffer[entry] = pygame.image.load(entry)
        return self.icon_buffer[entry]

    def update_all(self, now):
        if now - self.last_update >= self.update_cycle:
            self.last_update = now
            updated1 = self.update_AQI()
            updated2 = self.update_next24h_weather()
            updated3 = self.update_realtime_weather()
            updated4 = self.update_suggestion()
            return updated1 or updated2 or updated3 or updated4
        else:
            return False
    
    def render(self, window):
        anchor_x = 550
        anchor_y = 120
        x, y = anchor_x, anchor_y
        temp_font = window.get_font("NotoSansDisplay-Thin")
        text_font = window.get_font("苹方黑体-细-简")

        # 温度数值
        temp_surf, temp_rect = temp_font.render(self.realtime_info["temp"]+"°", (255,255,255), size=100)
        window.screen.blit(temp_surf, (x,y))
        x1, y1 = x+temp_rect.width+5, y+temp_rect.height+15

        # 天气描述
        descrip = self.realtime_info["text"] + "转" + self.next24h_info[0]["text"]
        descrip_surf, descrip_rect = text_font.render(descrip, (255,255,255), size=24)
        window.screen.blit(descrip_surf, (x, y1))

        # icons
        main_icon = self.get_icon(self.realtime_info["icon"], 256)
        small_icon1 = self.get_icon(self.next24h_info[0]["icon"], 64)
        small_icon2 = self.get_icon(self.next24h_info[1]["icon"], 64)
        main_icon = pygame.transform.scale(main_icon, (156,156))

        window.screen.blit(main_icon, (x1, y-20))
        x2 = x1+main_icon.get_rect().width-15
        window.screen.blit(small_icon1, (x2, y-3))
        y2 = y+small_icon1.get_rect().height
        window.screen.blit(small_icon2, (x2,y2))

        # 分割线
        y = y1+ descrip_rect.height + 20
        line = gradientRect((window.width-x, 2), (0,0,0), (255,255,255))
        window.screen.blit(line, (x, y))
        y += line.get_rect().height+5

        x += 10
        x_, y_ = (window.width+x)/2, y+56+10
        # 生活指数
        uv_icon         = pygame.image.load("./resources/Icon/UV_icon.png")
        uv_icon         = pygame.transform.scale(uv_icon, (56,56))
        hum_icon        = pygame.image.load("./resources/Icon/hum_icon.png")
        hum_icon        = pygame.transform.scale(hum_icon, (56,56))
        pressure_icon   = pygame.image.load("./resources/Icon/pressure_icon.png")
        pressure_icon   = pygame.transform.scale(pressure_icon, (56,56))
        AQI_icon        = pygame.image.load("./resources/Icon/AQI_icon.png")
        AQI_icon        = pygame.transform.scale(AQI_icon, (56,56))

        window.screen.blit(uv_icon, (x,y))
        window.screen.blit(AQI_icon, (x_, y))
        window.screen.blit(hum_icon, (x, y_))
        window.screen.blit(pressure_icon, (x_, y_))

        font = window.get_font("苹方黑体-准-简")

        blit_text_in_middle(window.screen, self.suggestion_info["UV指数"], font, 24, window.width, y+30, (255,255,255), (x+64, x_-10))
        blit_text_in_middle(window.screen, self.AQI_info[1], font, 24, window.width, y+30, (255,255,255), (x_+64, window.width))
        blit_text_in_middle(window.screen, self.realtime_info["humidity"]+"%", font, 24, window.width, y_+30, (255,255,255), (x+64, x_-10))
        blit_text_in_middle(window.screen, self.realtime_info["pressure"]+"Pa", font, 24, window.width, y_+30, (255,255,255), (x_+64, window.width))


if __name__ == "__main__":
    f = open("configs/config.yml")
    w = WeatherWidget(yaml.load(f)["weather"])
    w.get_next24h_weather()