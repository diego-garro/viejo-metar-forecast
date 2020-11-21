from metar import Metar
from datetime import datetime

oktas = {
    "FEW": '2',
    "SCT": '4',
    "BKN": '7',
    "OVC": '8'
}

convective = {
    None: '0',
    'TCU': '1',
    'CB': '2'
}

class MetarClass(Metar.Metar):
    
    NaN = 'NaN'
    
    def __init__(self, date, metar_text):
        super().__init__(metar_text, month=date.month, year=date.year)
        self.cavok = 1
        if metar_text.count('NIL') > 0:
            self.time = date
            self.cavok = MetarClass.NaN
    
    def get_wind_dir(self):
        if self.wind_dir is None:
            return MetarClass.NaN
        return self.wind_dir.value()
    
    def get_wind_speed(self):
        if self.wind_speed is None:
            return MetarClass.NaN
        return self.wind_speed.value()
    
    def get_wind_gust(self):
        if self.wind_gust is None:
            return MetarClass.NaN
        return self.wind_gust.value()
    
    def get_vis(self):
        if self.vis is None:
            return MetarClass.NaN
        if self.vis.value() < 10000.0:
            self.cavok = 0
        return self.vis.value()
    
    def get_weather(self, weather_code):
        for weather in self.weather:
            if weather_code in weather:
                self.cavok = 0
                return 1
        return 0
    
    def get_cavok(self):
        return self.cavok
    
    def get_sky_conditions(self):
        sky_conditions = [
            [MetarClass.NaN, MetarClass.NaN, MetarClass.NaN],
            [MetarClass.NaN, MetarClass.NaN, MetarClass.NaN],
            [MetarClass.NaN, MetarClass.NaN, MetarClass.NaN],
            [MetarClass.NaN, MetarClass.NaN, MetarClass.NaN],
        ]
        for layer in self.sky:
            if 'CLR' in layer:
                break
            if 'NSC' in layer:
                sky_conditions[0][0] = 'NSC'
                continue
            if 'VV' in layer:
                sky_conditions[0][0] = 'VV'
                if layer[1] is not None:
                    sky_conditions[0][1] = layer[1].value()
                sky_conditions[0][0] = 'VV'
                continue
            index = self.sky.index(layer)
            sky_conditions[index][0] = oktas[layer[0]]
            sky_conditions[index][1] = layer[1].value()
            sky_conditions[index][2] = convective[layer[2]]
            if layer[1] is not None:
                if layer[1].value() < 6000.0:
                    self.cavok = 0
        return sky_conditions