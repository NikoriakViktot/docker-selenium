import re
from abc import ABC, abstractmethod
import collections

from pymetdecoder import synop as s

class TelegramFactory:
    
    @staticmethod
    def create_telegram(type_telegram, **telegram):
        if type_telegram == 'hydro':
            return HydroTelegram(**telegram)
        elif type_telegram == 'meteo':
            return MeteoTelegram(type_telegram,**telegram)
        elif type_telegram == 'shtorm_hydro':
            return ShtormHydroTelegram(**telegram)
        else:
            raise ValueError("Invalid telegram type")



class Telegram(ABC):
 
    def __init__(self, **kwargs):
        self.index_station = kwargs['index_station']
        self.date_telegram = kwargs['date_telegram']
        self.time_telegram = kwargs['time_telegram']
        self.gauges_telegram = kwargs['gauges_telegram']
        self.date_time = self.date_telegram[8:]+self.time_telegram[:2]
        

    @abstractmethod
    def decoder(self):
        return DecoderFactory


class HydroTelegram(Telegram):

    Token = collections.namedtuple('Token', ['type', 'value'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.INDEX = r'(?P<INDEX>{})'.format(self.index_station)
        self.DATE_TIME = r'(?P<DATE_TIME>{}\d{{1}})'.format(self.date_time)
        self.WS = r'(?P<WS>\s+)'
        self.GROUP1 = r'(?P<GROUP1>1\d+)'
        self.GROUP2 = r'(?P<GROUP2>2\d+)'
        self.GROUP3 = r'(?P<GROUP3>3\d+)'
        self.GROUP4 = r'(?P<GROUP4>4\d+|4\d{2}//|4////)'
        self.GROUP5 = r'(?P<GROUP5>5\d+)'
        self.GROUP6 = r'(?P<GROUP6>6\d+)'
        self.GROUP7 = r'(?P<GROUP7>7\d+)'
        self.GROUP8 = r'(?P<GROUP8>8\d+)'
        self.GROUP0 = r'(?P<GROUP0>0\d+|0\d{3}/)'
        self.GROUP988 = r'(?P<GROUP988>988\d{2}\s0\d{4}|988\d{2}\s0\d{3}/)'
        self.GROUP966 = r'(?P<GROUP966>966\d{2}\s1\d{4}\s2\d{4}\s3\d{4}\s4\d{4}\s5\d{4}\s6\d{4}\s7\d{4}\s8\d{4}\s9\d{4})'
        self.END = r'(?P<END>=)'
        self.master_pat = re.compile('|'.join([
            self.WS,
            self.INDEX,  
            self.DATE_TIME,
            self.GROUP1,
            self.GROUP2,
            self.GROUP3,
            self.GROUP4,
            self.GROUP5,
            self.GROUP6,
            self.GROUP7,
            self.GROUP8,
            self.GROUP0,
            self.GROUP988,
            self.GROUP966,
            self.END
        ]))

    def decoder(self):
        return DecoderFactory
 
    def generate_tokens(self):
        scanner = self.master_pat.scanner(self.gauges_telegram)
        for m in iter(scanner.match, None):
            tok = self.Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok

    
    def parse(self): 
        self.tokens = self.generate_tokens() 
        self.tok = None 
        self.nexttok = None
        self._advance()
        parsed_telegram = self.expr()
       
        return parsed_telegram
         
    
    def _advance(self):
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None) 

    def _accept(self,toktype): 
        if self.nexttok and self.nexttok.type == toktype: 
            self._advance() 
            return True
        else:
            return False
        
    def _expect(self,toktype):
        if not self._accept(toktype): 
            raise SyntaxError('Expected ' + toktype)  

    def expr(self):
        parsed_telegram = {'groups': []}
    
        while self.nexttok is not None:
            group_type = self.nexttok.type
            group_value = self.nexttok.value
            if group_type in ['INDEX', 'DATE_TIME', 'GROUP1', 'GROUP2', 'GROUP3', 'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7', 'GROUP8', 'GROUP0', 'GROUP988', 'GROUP966']:
                parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            # self._advance()

        return parsed_telegram.get('groups')
    
    # def expr(self):
    #     parsed_telegram = {'groups': []}
    #     token_types = ['INDEX', 'DATE_TIME', 'GROUP1', 'GROUP2', 'GROUP3', 'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7', 'GROUP8', 'GROUP0', 'GROUP988', 'GROUP966']
    #     for toktype in token_types:
    #         while self._accept(toktype):
    #             group_type = self.tok.type
    #             group_value = self.tok.value
    #             parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
    #             self._advance()

        # while self._accept('INDEX') or self._accept('DATE_TIME') or self._accept('GROUP1') or self._accept('GROUP2') or self._accept('GROUP3') or \
        #     self._accept('GROUP4') or self._accept('GROUP5') or self._accept('GROUP6') or \
        #     self._accept('GROUP7') or self._accept('GROUP8') or self._accept('GROUP0'):
        #     group_type = self.tok.type
        #     group_value = self.tok.value
        #     parsed_telegram['groups'].append({'type': group_type, 'value': group_value})

       
        # while self._accept('GROUP988'):
        #     group_type = self.tok.type
        #     group_value = self.tok.value
        #     parsed_telegram['groups'].append({'type': group_type, 'value': group_value})

      
        # while self._accept('GROUP966'):
        #     group_type = self.tok.type
        #     group_value = self.tok.value
        #     parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
        
        # if group_type == 'DATE_TIME':
        #         date = group_value[:2]
        #         time = group_value[2:4]
        #         telegram_section_indicator = group_value[4]
        # decoder_type = group_type
        # decoder = self.decoder().create_decoder(decoder_type)  # Create the specific decoder
        # decoded_value = decoder.decode(group_value)        
        # parsed_telegram[group_type] = decoded_value
        # return parsed_telegram.get('groups')
    
class MeteoTelegram(Telegram):
    CODE_FM_12_IX_SYNOP = 'AAXX'
    Wind_speed_indicator = '1'
    
    def __init__(self, decoder_type,**kwargs):
        super().__init__(**kwargs)
        self.decoder_type = decoder_type
         
    

    def decoder(self):
        return super().decoder().create_decoder(self.decoder_type)
    
    def relative_telegam(self):
        station_type = self.CODE_FM_12_IX_SYNOP
        obs_time = self.date_time+self.Wind_speed_indicator
        telegram = station_type + ' ' + obs_time + ' ' + self.gauges_telegram.rstrip('=')
        return self.decoder().decode(telegram) 
    

    


class ShtormHydroTelegram(Telegram):
    def interpret(self):
        pass
        # Реалізація для ShtormHydroTelegram    


class AbstractDecoder(ABC):
    @abstractmethod
    def decode(self, value):
        pass

    def create_dict(self, *args):
        key = f"{self.__class__.__name__.lower().rstrip('decoder')}"
        return {key: dict(zip(args[::2], args[1::2]))}


class IndexStationDecoder(AbstractDecoder):
    def decode(self, value):
        return self.create_dict('value', value, 'number_basyen', value[0:2], 'number_station', value[2:])


class ObsTimeDecoder(AbstractDecoder):
    def decode(self, value):
        return self.create_dict('day', value[:2], 'hour', value[0:2], 'telegram_section_indicator', value[4])


class WaterLevelDecoder(AbstractDecoder):
    def _decode_value(self, value):
        try:
            match value[0]:
                case 0 | 1 | 2 | 3 | 4: return self.create_dict('water_level', int(value[0:4]), 'unit', 'cm')
                case 5: return self.create_dict('water_level', -(int(value[1:4])), 'unit', 'cm')
                case 6: return self.create_dict('water_level', -((int(value[1:4])) + 1000), 'unit', 'cm')
                case _: return None
        except:
            return None

    def decode(self, value):
        if value[0] == '1':
            return self._decode_value(value[1:])
        elif value[0] == '3':
            return self._decode_value(value[1:])


class WaterLevelChangeDecoder(AbstractDecoder):
    def _decode_value(self, value):
        try:
            match int(value[4]):
                case 0: return 0
                case 1: return int(value[1:4])
                case 2: return -(int(value[1:4]))
                case _: return None
        except:
            if len(value) != 5:
                raise ValueError('невірна кількість цифр')
            

    def decode(self, value):
        return self.create_dict('value', self._decode_value(value))
    

class TemperatureDecoder(AbstractDecoder):
    def decode(self, value):
        # Ваш код тут
        return self._decode_value(value)
    
    def _decode_value(self, value):
        try:
            match value[3]:
                case '5': return -(float(int(value[4]))) 
                case '6': return -(float(int(value[4])+10))
                case '7': return -(float(int(value[4])+20))
                case '8': return -(float(int(value[4])+30))
                case '9': return -(float(int(value[4])+40))
                case _: return float(int(value[3:]))
        except:
            return  None
    

class IcePhenomenaDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        # Ваш код тут
       pass

class WaterBodyConditionDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        # Ваш код тут
        pass          

class IceThicknessDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        # Ваш код тут
        pass
    
class WaterDischargeDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        # Ваш код тут
        pass


class DailyPrecipitationDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        try:

            match value[1:4]:
                case '000': return None
                case '990'|'991'|'992'|'993'|'994'|'995'|'996'|'997'|'998'|'999':
                    return float((int(value[2:4]) - 90)/10)
                case _: return float(value[1:4])
        except:
            return None


    
class DailyDaytimePrecipitationDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        # Ваш код тут
        pass
    
    

class MeasuredWaterDischargeDecoder(AbstractDecoder):
    def decode(self, value, date_time):
        pass
        # return decoded_value




class MeteoDecoder(AbstractDecoder):

    def __init__(self):
        self.decoder = s.SYNOP()

    def decode(self, telegram):
        return self.decoder.decode(telegram)
    
class DecoderFactory:
    decoders = {
            'meteo' : MeteoDecoder,
            'INDEX': IndexStationDecoder,
            'DATE_TIME' : ObsTimeDecoder,
            'GROUP1': WaterLevelDecoder,
            'GROUP2': WaterLevelChangeDecoder,
            'GROUP3': WaterLevelDecoder,
            'GROUP4': TemperatureDecoder,
            'GROUP5': IcePhenomenaDecoder,
            'GROUP6': WaterBodyConditionDecoder,
            'GROUP7': IceThicknessDecoder,
            'GROUP8': WaterDischargeDecoder,
            'GROUP0': DailyPrecipitationDecoder,
            'GROUP988': DailyDaytimePrecipitationDecoder,
            'GROUP966': MeasuredWaterDischargeDecoder
            }
    
    
    @classmethod
    def create_decoder(cls, type):
        decoder_class = cls.decoders.get(type)
        if decoder_class:
            return decoder_class()
        else:
            raise ValueError(f"Decoder type '{type}' not recognized")
        


d ={'date_telegram': '2023-06-04', 
    'time_telegram': '08:00:00', 
    'index_station': '81041',
    'gauges_telegram': '81041 04081 10262 20062 30265 41912 52201 56565 54506 66666 61111 82980 0000/ 98803 0000/ 96606 11223 23555 34555 46666 55555 66666 77777 88888 99999='}
telegram_obj = TelegramFactory.create_telegram('hydro', **d)
decoded_telegram = telegram_obj.parse()    
print([x for x in telegram_obj.generate_tokens()])
print(decoded_telegram)

