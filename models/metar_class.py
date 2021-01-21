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
    null = 'null'
    
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
    
    def _return_value_else_null(self, var):
        return str(var.value()) if var != None else MetarClass.null
    
    def _return_weather_else_null(self, *args):
        for arg in args:
            for tup in self.weather:
                if arg in tup:
                    return arg
        return MetarClass.null
    
    def _return_sky_layer_or_null(self, index, parameter='cover'):
        """Return the value of interest in the sky variable of METAR.

        Args:
            index (int): Index of the layer to search.
            parameter (str, optional): Parameter of the layer to extract. Defaults to 'cover'.
                options: 'height', 'cloud'
        """
        if len(self.sky) > index:
            if parameter == 'cover':
                return self.sky[index][0]
            elif parameter == 'height':
                if self.sky[index][1] != None:
                    return str(self.sky[index][1].value())
                else:
                    return MetarClass.null
            elif parameter == 'cloud':
                if self.sky[index][2] is None:
                    return MetarClass.null
                return self.sky[index][2]
        return MetarClass.null
    
    def _return_temperature_or_null(self, type='absolute'):
        """Return the temperature absolute or dewpoint or null.

        Args:
            type (str, optional): Type of temperature. Defaults to 'absolute'.
                options: 'dewpoint'
        """
        if type == 'absolute':
            if self.temp is not None:
                return str(self.temp.value())
        elif type == 'dewpoint':
            if self.dewpt is not None:
                return str(self.dewpt.value())
        return MetarClass.null
    
    def _return_pressure_or_null(self):
        if self.press is not None:
            return str(self.press.value())
        return MetarClass.null
    
    def to_dict(self):
        d = {
            "date": datetime.strftime(self.time, "%Y%m%d%H%M"),
            "year": str(self.time.year),
            "month": str(self.time.month),
            "day": str(self.time.day),
            "hour": str(self.time.hour),
            "minute": str(self.time.minute),
            "type": self.type,
            "station": self.station_id,
            "wind_direction": self._return_value_else_null(self.wind_dir),
            "wind_speed": self._return_value_else_null(self.wind_speed),
            "wind_gust": self._return_value_else_null(self.wind_gust),
            "visibility": self._return_value_else_null(self.vis),
            "weather_intensity": self._return_weather_else_null('+', '-', 'VC'),
            "weather_description": self._return_weather_else_null('SH', 'TS', 'BC'), 
            "weather_precipitation": self._return_weather_else_null('RA', 'DZ'),
            "weather_obscuration" : self._return_weather_else_null('FG', 'BR'),
            "sky_layer1_cover": self._return_sky_layer_or_null(0),
            "sky_layer1_height": self._return_sky_layer_or_null(0, parameter='height'),
            "sky_layer1_cloud": self._return_sky_layer_or_null(0, parameter='cloud'),
            "sky_layer2_cover": self._return_sky_layer_or_null(1),
            "sky_layer2_height": self._return_sky_layer_or_null(1, parameter='height'),
            "sky_layer2_cloud": self._return_sky_layer_or_null(1, parameter='cloud'),
            "sky_layer3_cover": self._return_sky_layer_or_null(2),
            "sky_layer3_height": self._return_sky_layer_or_null(2, parameter='height'),
            "sky_layer3_cloud": self._return_sky_layer_or_null(2, parameter='cloud'),
            "sky_layer4_cover": self._return_sky_layer_or_null(3),
            "sky_layer4_height": self._return_sky_layer_or_null(3, parameter='height'),
            "sky_layer4_cloud": self._return_sky_layer_or_null(3, parameter='cloud'),
            "temperature": self._return_temperature_or_null(),
            "dewpoint": self._return_temperature_or_null(type='dewpoint'),
            "pressure": self._return_pressure_or_null(),
            "code": self.code.strip(),
        }
        
        return d