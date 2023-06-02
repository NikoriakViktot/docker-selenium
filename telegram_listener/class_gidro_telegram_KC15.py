import re

# from class_station_index.class_gidro_station_index import Gidro_station_index


class GidroTelegrame:

    def __init__(self, **kwargs):
        self.index_hydro_station = kwargs.get('index_station')
        self.date_telegram = kwargs.get('date_telegram')
        self.__time_telegram = kwargs.get('time_telegram')
        self.gauges_telegrame = kwargs.get('gauges_telegrame')
        self.telegrame_split = kwargs.get('gauges_telegrame')
        self._telegram_report = self.telegram_report
        self._telegrame = kwargs.get('gauges_telegrame')




    @property
    def index_hydro_station(self):
        return self._index

    @index_hydro_station.setter
    def index_hydro_station(self, index):
        self._index = index

    @property
    def date_telegram_(self):
        return self.date_telegram[0:10]

    @property
    def time_telegram(self):
        # if ''.__eq__(self._date_telegram[11:]):
        #     return None
        # else:
        return self.__time_telegram


    @property
    def gauges_telegrame_(self):
        return self._telegrame

    @gauges_telegrame_.setter
    def gauges_telegrame_(self, telegrame):
        try:
            self._telegrame = telegrame
        except:
            self._telegrame = None


    @property
    def telegrame_split(self):
        return self._telegrame_split

    @telegrame_split.setter
    def telegrame_split(self, telegrame_split):
        try:
            telegram_split = [re.sub(("="), "", i) for i in [y for y in telegrame_split.split(' ')]]
            self._telegrame_split = tuple(telegram_split)
        except:
            self._telegrame_split = None

    @property
    def telegram_report(self):
        if self.gauges_telegrame is None:
            return self._index, False
        else:
            return self._index, True



class KC15(GidroTelegrame):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.value = self.telegrame_split


    @property
    def telegram_index(self):
        try:
            return self.telegrame_split[0]
        except:
            if self.telegram_report[1] is False:
                return self.telegram_report

    @property
    def telegram_date(self):
        try:
           return self.telegrame_split[1][0:2]
        except:
           return None

    @property
    def telegram_time(self):
        try:
            return self.telegrame_split[1][2:4]
        except:
            if self.telegram_report[1] is False:
                return None

    @property
    def telegram_type(self):
        try:
            return self.telegrame_split[1][4:5]
        except:
            return None

    @property
    def index_gidro_station_group(self):
        try:
            match = re.match('\d{5}', self.value[0])
            return match.string
        except:
            if self.telegram_report[1] is False:
                return  None



    @property
    def observation_period_group(self):
        try:
            match = re.match('\d{5}', self.value[1])
            if (match is None) or (len(self.value[1]) != 5):
                raise ValueError('невірна кількість цифр')
            return match.string
        except:
            return None



    @property
    def water_level_group(self):
        try:
            water_level = self.value[2:]
            match = [i for i in [re.search('1\d{4}', x) for x in water_level] if i != None][0].string
            return match
        except:
            return None



    @property
    def level_change_group(self):
        try:
            level_change = self.value[2:]
            match = [i for i in [re.search('2\d{4}', x) for x in level_change] if i != None][0].string
            return match
        except:
            return None

    @property
    def water_level_20_00_group(self):
        try:
            water_level = self.value[2:8]
            match = [i for i in [re.search('3\d{4}', x) for x in water_level] if i != None][0].string
            return match
        except:
            return None



    @property
    def temperature_group(self):
        try:
            temperature = self.value[2:8]
            match = [i for i in [re.search('4\d{4}|4\d{2}//|4////', x) for x in temperature] if i != None][0].string
            return match
        except:
            return None



    @property
    def ice_observations_group(self):
        try:
            ice_observations = self.value[2:9]
            match = [i.string for i in [re.search('5\d{4}', x) for x in ice_observations] if i != None]
            if match:
                return match
            else:
                return None
        except:
            return None



    @property
    def status_object_water_group(self):
        try:
            status_object_water = self.value[2:9]
            match = [i.string for i in [re.search('6\d{4}', x) for x in status_object_water] if i != None]
            if match:
                return match
            else:
                return None
        except:
            return None


    @property
    def ice_thickness_group(self):
        try:
            ice_thickness = self.value[2:]
            match = [i for i in [re.search('7\d{4}', x) for x in ice_thickness] if i != None][0].string
            return match
        except:
            return None



    @property
    def water_discharge_group(self):
        try:
            water_discharge = self.value[2:]
            match = [i for i in [re.search('8\d{4}', x) for x in water_discharge] if i != None][0].string
            return match
        except:
            return None



    @property
    def precipitation_day_group(self):
        try:
            precipitation = self.value[2:]
            match = [i for i in [re.search('0\d{4}|0\d{3}/', x) for x in precipitation] if i != None][0].string
            if match is not None:
                return match
        except:
            return None



    @property
    def precipitation_daytime_group(self):
        try:
            precipitation = self.value[2:]
            match = [i for i in [re.search('0\d{4}|0\d{3}/', x) for x in precipitation] if i != None][1].string
            match1 = [i.string for i in [re.search('988\d{2}', x) for x in precipitation] if i != None][0]
            precipitation_daytime=match1,match
            if precipitation_daytime is not None:
                return precipitation_daytime

        except:
            return None



    @property
    def measured_water_discharge_group(self):
        try:
            water_discharge = self.gauges_telegrame
            match = [i.group().split(' ') for i in [re.search('((966\d{2}).*(9\d{4}))', water_discharge)]][0]
            if match:
                return match
            else:
                return None
        except:
            return None


    @property
    def measured_past_days_group(self):
        try:
            water_masured = self.gauges_telegrame
            past_days = re.sub(("="), "", water_masured)
            match = [i.group().split(' ') for i in [re.search('((922\d{2}).*)', past_days)]][0]
            if match:
                return match
            else:
                return None
        except:
            return None


    @property
    def measured_max_days_group(self):
        try:
            water_masured = self.gauges_telegrame
            past_days = re.sub(("="), "", water_masured)
            match = [i.group().split(' ') for i in [re.search('((933\d{2}).*)', past_days)]][0]
            if match:
                return match
            else:
                return None
        except:
            return None


    def water_level_08(self):
        try:
            value = self.water_level_group
            match int(value[1]):
                case 0|1|2|3|4: return int(value[1:5])
                case 5: return -(int(value[2:5]))
                case 6: return -((int(value[2:5]))+1000)
                case _: return None
        except:
            return None



    def level_change(self):
        try:
            match int(self.level_change_group[4]):
                case 0: return 0
                case 1: return int(self.level_change_group[1:4])
                case 2: return -(int(self.level_change_group[1:4]))
                case _: return None
        except:
            return None



    def water_level_20_00(self):
        try:
            value = self.water_level_20_00_group
            match int(value[1]):
                case 0 | 1 | 2 | 3 | 4:
                    return int(value[1:5])
                case 5: return -(int(value[2:5]))
                case 6: return -((int(value[2:5])) + 1000)
                case _: return None
        except:
            return None



    def precipitation_day(self):
        try:
            value = self.precipitation_day_group
            match value[1:4]:
                case '000': return None
                case '990'|'991'|'992'|'993'|'994'|'995'|'996'|'997'|'998'|'999':
                    return float((int(value[2:4]) - 90)/10)
                case _: return float(value[1:4])

        except:
            return None


    def precipitation_day_intensity(self):
        try:
            value_precipitation_intensity = self.precipitation_day_group[4]
            if self.precipitation_day() is not None:
                match value_precipitation_intensity:
                    case '0': return '> 1'
                    case '1': return '1 - 3'
                    case '2': return '3 - 6'
                    case '3': return '6 - 12'
                    case '4': return '< 12'
                    case '/': return None
                    case _:   return None

        except:
            return None



    def precipitation_daytime(self):
        try:
            value_precipitation = self.precipitation_daytime_group[1]
            value_day = self.precipitation_daytime_group[0][3:5]
            match value_precipitation[1:4]:
                case '000': return None
                case '990'|'991'|'992'|'993'|'994'|'995'|'996'|'997'|'998'|'999':
                    return float((int(value_precipitation[2:4]) - 90)/10)
                case _: return float(value_precipitation[1:4])
        except:
            return None


    def precipitation_daytime_intensity(self):
        try:
            value_precipitation_intensity = self.precipitation_daytime_group[1][4]
            if self.precipitation_daytime() is not None:
                match value_precipitation_intensity:
                    case '0': return '> 1'
                    case '1': return '1 - 3'
                    case '2': return '3 - 6'
                    case '3': return '6 - 12'
                    case '4': return '< 12'
                    case '/': return None
                    case _:   return None


        except:
            return None



    def water_discharge(self):
        try:
            value = self.water_discharge_group
            match int(value[1]):
                case 0: return float(int(value[2:5])/1000)
                case 1: return float(int(value[2:5])/100)
                case 2: return float((int(value[2:5]))/10)
                case 3: return float(value[2:5])
                case 4: return float(int(value[2:5])*10)
                case 5: return float(int(value[2:5])*100)
                case _: return None
        except:
            return None



    def temperature_water(self):
        try:



            return float(int(self.temperature_group[1:3]))


        except:
            return self.index_gidro_station_group, None



    def temperature_air(self):
        try:
            value = self.temperature_group[3:]
            match value[3]:
                # case '/': return None
                case '5': return -(float(int(value[4])))
                case '6': return -(float(int(value[4])+10))
                case '7': return -(float(int(value[4])+20))
                case '8': return -(float(int(value[4])+30))
                case '9': return -(float(int(value[4])+40))
                case _: return float(int(value))
        except:
            return  None



    def report(self):
        report = [self.telegram_report[1],
                  self.index_hydro_station,
                  self.date_telegram_,
                  self.time_telegram,
                  self.observation_period_group,
                  self.water_level_08(),
                  self.level_change(),
                  self.water_level_20_00(),
                  self.temperature_air(),
                  self.water_discharge(),
                  self.precipitation_day(),
                  self.precipitation_day_intensity(),
                  self.precipitation_daytime(),
                  self.precipitation_daytime_intensity(),
                  self.gauges_telegrame_]
        return tuple(report)


    def __call__(self, *args, **kwargs):
        return self.report()

