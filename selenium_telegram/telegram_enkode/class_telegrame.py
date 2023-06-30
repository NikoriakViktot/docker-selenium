import re
from abc import ABC, abstractmethod

class Telegram(ABC):
    def __init__(self, telegram):
        self.telegram = telegram

    @abstractmethod
    def interpret(self):
        pass

class HydroTelegram(Telegram):
    def interpret(self):
        pass
        # Реалізація для HydroTelegram


class MeteoTelegram(Telegram):
    def interpret(self):
        pass
        # Реалізація для MeteoTelegram

class ShtormHydroTelegram(Telegram):
    def interpret(self):
        pass
        # Реалізація для ShtormHydroTelegram

class TelegramFactory:
    @staticmethod
    def create_telegram(type_telegram, telegram):
        if type_telegram == 'hydro':
            return HydroTelegram(telegram)
        elif type_telegram == 'meteo':
            return MeteoTelegram(telegram)
        elif type_telegram == 'shtorm_hydro':
            return ShtormHydroTelegram(telegram)
        else:
            raise ValueError("Invalid telegram type")




    def telegrame_split(self):
        try:
            telegram_split =  re.findall(r'\b\d+\b|=+', self.telegram)
            # [re.sub(("="), "", i) for i in [y for y in self.gauges_telegrame.split(' ')]]
            self._telegrame_split = tuple(telegram_split)
        except:
            self._telegrame_split = None

class KS15:
    def __get__(self, instance, owner):
        return self.decode(instance)

    def decode(self, telegram):
        # decoding logic for HydroTelegram using telegram._telegram_split
        pass

            
# class HydroTelegram(Telegram):
#     def decode(self):
#         # decoding logic for HydroTelegram
#         pass

# class MeteoTelegram(Telegram):
#     def decode(self):
#         # decoding logic for MeteoTelegram
#         pass

# class TelegramFactory:
#     @staticmethod
#     def create_telegram(type_telegram, telegram):
#         if type_telegram == 'hydro':
#             return HydroTelegram(telegram)
#         elif type_telegram == 'meteo':
#             return MeteoTelegram(telegram)
#         else:
#             raise ValueError("Invalid telegram type")    
import re


token_patterns = {
    'INDEX': r'\d{5}',
    'DATE_TIME': r'\d{5}',
    'GROUP1': r'1\d{4}',
    'GROUP2': r'2\d{4}',
    'GROUP3': r'3\d{4}',
    'GROUP4': r'4\d{4}|4\d{2}//|4////',
    'GROUP5': r'5\d{4}',
    'GROUP6': r'6\d{4}',
    'GROUP7': r'7\d{4}',
    'GROUP8': r'8\d{4}',
    'GROUP0': r'0\d{4}|0\d{3}/',
    'GROUP988':r'988\d+',
    'PRECIPITATION':r'0\d{4}|0\d{3}/'
}


def process_tokens(input_text):
    input_text = input_text.rstrip('=')  # Видалення "=" з кінця рядка
    tokens = input_text.split()
    groups = {}
    all_groups = ['GROUP1', 'GROUP2', 'GROUP3', 'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7', 'GROUP8', 'GROUP0', 'GROUP988', 'PRECIPITATION']
    for group_name, pattern in token_patterns.items():
        if group_name in all_groups:
            if tokens and pattern and re.match(pattern, tokens[0]):
                groups[group_name] = tokens.pop(0)
            else:
                groups[group_name] = None
        else:
            groups[group_name] = tokens.pop(0) if tokens else None
            if groups[group_name] and pattern and not re.match(pattern, groups[group_name]):
                groups[group_name] = None
    
    print("Groups:")
    for group_name, group_value in groups.items():
        print(f"{group_name}: {group_value}")
# input_text = '42148 23081 10048 20021 30056 42123 83123 00000 98822 00000='

# Регулярні вирази для токенів

# Розбиття на токени за допомогою регулярних виразів
import re
from collections import namedtuple
class TokenDescriptor:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern
    
    def __get__(self, instance, owner):
        return instance._tokens.get(self.name, None)
    
    def __set__(self, instance, value):
        if value is not None and not re.match(self.pattern, value):
            value = None
        instance._tokens[self.name] = value

class TokenProcessor:
    # INDEX = TokenDescriptor('INDEX', r'\d{5}')
    # DATE_TIME = TokenDescriptor('DATE_TIME', r'\d{5}')
    # GROUP1 = TokenDescriptor('GROUP1', r'1\d{4}')
    # GROUP2 = TokenDescriptor('GROUP2', r'2\d{4}')
    # GROUP3 = TokenDescriptor('GROUP3', r'3\d{4}')
    # GROUP4 = TokenDescriptor('GROUP4', r'4\d{4}|4\d{2}//|4////')
    # GROUP5 = TokenDescriptor('GROUP5', r'5\d{4}')
    # GROUP6 = TokenDescriptor('GROUP6', r'6\d{4}')
    # GROUP7 = TokenDescriptor('GROUP7', r'7\d{4}')
    # GROUP8 = TokenDescriptor('GROUP8', r'8\d{4}')
    # GROUP0 = TokenDescriptor('GROUP0', r'0\d{4}|0\d{3}/')
    # GROUP988 = TokenDescriptor('GROUP988', r'988\d+')
    # PRECIPITATION = TokenDescriptor('PRECIPITATION_LAST_DAY', r'\0\d{4}|0\d{3}/')
    INDEX = r'(?P<INDEX> \d{5})'
    DATE_TIME = r'(?P<DATE_TIME>\d{5})'
    GROUP1 = r'(?P<GROUP1>1\d{4})'
    GROUP2 = r'(?P<GROUP2>2\d{4})'
    GROUP3 = r'(?P<GROUP3>3\d{4})'
    GROUP4 = r'(?P<GROUP4>4\d{4}|4\d{2}//|4////)'
    GROUP5 = r'(?P<GROUP5>5\d{4})'
    GROUP6 = r'(?P<GROUP6>6\d{4})'
    GROUP7 = r'(?P<GROUP7>7\d{4})'
    GROUP8 = r'(?P<GROUP8>8\d{4})'
    GROUP0 = r'(?P<GROUP0>0\d{4}|0\d{3}/)'
    GROUP988 = r'(?P<GROUP988>988\d{2}\s0\d{4}|988\d{2}\s0\d{3}/)'
    PRECIPITATION = r'(?P<PRECIPITATION_LAST_DAY>0\d{4}|0\d{3}/)'
    WS = r'(?P<WS>\s+)'
    GROUP966= r'(?P<GROUP966>966\d{2}\s1\d{4}\s2\d{4}\s3\d{4}\s4\d{4}\s5\d{4}\s6\d{4}\s7\d{4}\s8\d{4}\s9\d{4})' 
    master_pat = re.compile('|'.join([GROUP1, GROUP2, GROUP3,
                   GROUP4, GROUP5, GROUP6, GROUP7, GROUP8, 
                    GROUP0, GROUP988, WS, GROUP966]))
    all_groups = ['INDEX', 'DATE_TIME', 'GROUP1', 'GROUP2', 'GROUP3',
                   'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7', 'GROUP8', 
                    'GROUP0', 'GROUP988', 'PRECIPITATION']

    # def __init__(self, input_text):
    #     input_text = input_text.rstrip('=')  # Видалення "=" з кінця рядка
    #     self._tokens = {}
    #     tokens = input_text.split()
    #     for group_name, pattern in token_patterns.items():
    #         if group_name in self.all_groups:
    #             if tokens and pattern and re.match(pattern, tokens[0]):
    #                 self._tokens[group_name] = tokens.pop(0)
    #             else:
    #                 self._tokens[group_name] = None
    #         else:
    #             self._tokens[group_name] = None
    #             tokens.pop(0) if tokens else None

    #         if self._tokens[group_name] and pattern and not re.match(pattern, self._tokens[group_name]):
    #             self._tokens[group_name] = None
 

    def process(self):
        print("Groups:")
        for name, value in self._tokens.items():
            print(f"{name}: {value}")
    
    
    
    @staticmethod
    def generate_tokens(pat, text):
       Token = namedtuple('Token', ['type', 'value'])
       scanner = pat.scanner(text)
       for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

    def token(self, text):
        input_text = text.rstrip('=')
        tokens = (tok for tok in self.generate_tokens(self.master_pat, input_text[12:]) if tok.type != 'WS')
        for tok in tokens:
            print(tok)
            if tok.type == 'GROUP0':
                continue  

        # for tok in (self.master_pat, ):
        #     print(tok) 
        #     if tok.type == 'GROUP0':
        #         continue  
# Створення об'єкту TokenProcessor і обробка токенів


# Вхідний текст для розбиття на токени
input_text = ['42148 23081 10048 20021 30056 42123 83123 00050 98822 00052=',
'42187 04081 10054 20052 30058 82166 00000 98803 00000 96606 11223 23555 34555 46666 55555 66666 77777 88888 99999=',
'42194 04081 10116 20012 30116 48808 00011 98803 00051=',
'81041 04081 10262 20062 30265 41912 52201 56565 54506 82980 0000/ 98803 0000/=',
'44033 04081 10149 20012 30149 00052=',
'42256 04081 10174 20000 30174 49308 00021 98803 02211=',
'42256 05081 10174 20000 30174 41111 00000 98804 00000=',
'79361 05081 10266 20032 30267 62305 81690 0000/=']
# Розбиття на токени за допомогою регулярного виразу
# for line in input_text:
#     # tokens = re.findall('|'.join(token_regexes), line)
#     # process_tokens(line)
#     # processor = TokenProcessor(line)
#     # processor.process()
#     t = TokenProcessor()
#     t.token(line)

import re
import collections

# Определение токенов
    # index_station = ''
    # date_telegram = ''
    # time_telegram = '' 
    # gauges_telegram = ''
    # INDEX = r'(?P<INDEX>{})'.format(index_station)
    # DATE_TIME = r'(?P<DATE_TIME>{}{}\d)'.format(date_telegram, time_telegram)
    # WS = r'(?P<WS>\s+)'
    # GROUP1 = r'(?P<GROUP1>1\d{4})'
    # GROUP2 = r'(?P<GROUP2>2\d{4})'
    # GROUP3 = r'(?P<GROUP3>3\d{4})'
    # GROUP4 = r'(?P<GROUP4>4\d{4}|4\d{2}//|4////)'
    # GROUP5 = r'(?P<GROUP5>5\d{4})'
    # GROUP6 = r'(?P<GROUP6>6\d{4})'
    # GROUP7 = r'(?P<GROUP7>7\d{4})'
    # GROUP8 = r'(?P<GROUP8>8\d{4})'
    # GROUP0 = r'(?P<GROUP0>0\d{4}|0\d{3}/)'
    # GROUP988 = r'(?P<GROUP988>988\d{2}\s0\d{4}|988\d{2}\s0\d{3}/)'
    # # PRECIPITATION = r'(?P<PRECIPITATION_LAST_DAY>0\d{4}|0\d{3}/)'
    # GROUP966 = r'(?P<GROUP966>966\d{2}\s1\d{4}\s2\d{4}\s3\d{4}\s4\d{4}\s5\d{4}\s6\d{4}\s7\d{4}\s8\d{4}\s9\d{4})'

    # master_pat = re.compile('|'.join([INDEX, DATE_TIME, WS, 
    #                                   GROUP1, GROUP2, GROUP3,
    #                                   GROUP4, GROUP5, GROUP6, 
    #                                   GROUP7, GROUP8, GROUP0,
    #                                   GROUP988, GROUP966]))
        # GidroTelegram.index_station = kwargs['index_station']
        # GidroTelegram.date_telegram = kwargs['date_telegram'][8:]
        # GidroTelegram.time_telegram = kwargs['time_telegram'][:2]
        # GidroTelegram.gauges_telegram = kwargs['gauges_telegram']
class GidroTelegram:

    # # Токенизатор
    Token = collections.namedtuple('Token', ['type', 'value'])

    def __init__(self, **kwargs):
        self.index_station = kwargs['index_station']
        self.date_telegram = kwargs['date_telegram'][8:]
        self.time_telegram = kwargs['time_telegram'][:2]
        self.gauges_telegram = kwargs['gauges_telegram']
        self.d = self.date_telegram+self.time_telegram
        self.INDEX = r'(?P<INDEX>{})'.format(self.index_station)
        self.DATE_TIME = r'(?P<DATE_TIME>{}1)'.format(self.d)
        self.WS = r'(?P<WS>\s+)'
        self.GROUP1 = r'(?P<GROUP1>1\d{4})'
        self.GROUP2 = r'(?P<GROUP2>2\d{4})'
        self.GROUP3 = r'(?P<GROUP3>3\d{4})'
        self.GROUP4 = r'(?P<GROUP4>4\d{4}|4\d{2}//|4////)'
        self.GROUP5 = r'(?P<GROUP5>5\d{4})'
        self.GROUP6 = r'(?P<GROUP6>6\d{4})'
        self.GROUP7 = r'(?P<GROUP7>7\d{4})'
        self.GROUP8 = r'(?P<GROUP8>8\d{4})'
        self.GROUP0 = r'(?P<GROUP0>0\d{4}|0\d{3}/)'
        self.GROUP988 = r'(?P<GROUP988>988\d{2}\s0\d{4}|988\d{2}\s0\d{3}/)'
        self.GROUP966 = r'(?P<GROUP966>966\d{2}\s1\d{4}\s2\d{4}\s3\d{4}\s4\d{4}\s5\d{4}\s6\d{4}\s7\d{4}\s8\d{4}\s9\d{4})'
        self.END = r'(?P<END>=)'
        self.master_pat = re.compile('|'.join([
            self.WS,
            self.INDEX,  # Використовуємо значення змінних
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

      
 
    def generate_tokens(self):
        scanner = self.master_pat.scanner(self.gauges_telegram)
        for m in iter(scanner.match, None):
            tok = self.Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok

    
    def parse(self): 
        self.tokens = self.generate_tokens() 
        # Последний потребленный символ 
        self.tok = None 
        # Следующий токенизированный символ 
        self.nexttok = None
        # Загрузить первый токен предварительного просмотра
        self._advance()
        parsed_telegram = self.expr()
        return parsed_telegram
         
    
    def _advance(self):
        'Продвинуться на один токен вперед'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None) 

    def _accept(self,toktype): 
        'Проверить и потребить следующий токен, если он совпадает с toktype'
        if self.nexttok and self.nexttok.type == toktype: 
            self._advance() 
            return True
        else:
            return False
        
    def _expect(self,toktype):
        'Потребить следующий токен, если он совпадает с toktype, или возбудить SyntaxError' 
        if not self._accept(toktype): 
            raise SyntaxError('Expected ' + toktype)  

    # Далее следуют правила грамматики
    
    def expr(self):
        parsed_telegram = {'groups': []}
        if self._accept('INDEX'):
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()
        
        # Перевірити наявність токену 'DATE_TIME'
        if self.tok.type == 'DATE_TIME':
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()

        # Шукати групи GROUP1-8
        if self._accept('GROUP1') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()

        if self._accept('GROUP2') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()  

        if self._accept('GROUP3') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()    

        if self._accept('GROUP4') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()    
        
        if self._accept('GROUP5') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()    
        if self._accept('GROUP6') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance() 

        if self._accept('GROUP7') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()    

        if self._accept('GROUP8') :
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()    
     

        # Шукати групу GROUP0
        if self._accept('GROUP0'):
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()

        # Шукати групу GROUP988
        if self._accept('GROUP988'):
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()

        # Шукати групу GROUP966
        if self._accept('GROUP966'):
            group_type = self.tok.type
            group_value = self.tok.value
            parsed_telegram['groups'].append({'type': group_type, 'value': group_value})
            self._advance()
        parsed_telegram['term'] = self.term()
        return parsed_telegram.get('groups')
    
    
    def term(self):
        termval = self.factor()
        while self._accept('WS'):
            pass  # Пропуск пробільних символів

        while self._accept('INDEX') or self._accept('DATE_TIME') or self._accept('GROUP1') or \
            self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
            self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or \
            self._accept('GROUP8') or \
            self._accept('GROUP0') or self._accept('GROUP988') or \
            self._accept('GROUP966') or self._accept('END'): 
            op = self.tok.type
            right = self.factor()
            termval = (op, termval, right)
        
        return termval

    # def factor(self):
   
    #     if self._accept('WS'):
    #         pass  # Пропуск пробільних символів

    #     if self._accept('INDEX') or self._accept('DATE_TIME') or self._accept('GROUP1') or \
    #           self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
    #           self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or \
    #           self._accept('GROUP8') or \
    #           self._accept('GROUP0') or self._accept('GROUP988') or \
    #           self._accept('GROUP966') or self._accept('END'): 
    #         return self.tok.value
    #     else:
    #         raise SyntaxError('Invalid token: ' + self.nexttok.type)
          
    def factor(self):
        if self._accept('WS'):
            pass  # Пропуск пробільних символів

        if self._accept('INDEX') or self._accept('DATE_TIME') or self._accept('GROUP1') or \
            self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
            self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or \
            self._accept('GROUP8') or \
            self._accept('GROUP0') or self._accept('GROUP988') or \
            self._accept('GROUP966') or self._accept('END'): 
            return self.tok.value
        else:
            raise SyntaxError('Invalid token: ' + (self.nexttok.type if self.nexttok else 'None'))


        
              

d ={'date_telegram': '2023-06-05', 
    'time_telegram': '08:00:00', 
    'index_station': '42187',
    'gauges_telegram': '42187 04081 10054 20052 30058 82166 00000 98803 00000 96606 11223 23555 34555 46666 55555 66666 77777 88888 99999='}
    
s = GidroTelegram(**d)
s.parse()
print([x for x in s.generate_tokens()])
print(s.parse())

class ExpressionTreeBuilder:
    def __init__(self):
        self.tokens = None
        self.tok = None
        self.nexttok = None
        self._advance()

    def parse_expression_tree(self, text):
        self.tokens = generate_tokens(text)
        self._advance()
        return self.expr()

    def _advance(self):
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    def expr(self):
        "expression ::= term { ('+'|'-') term }"

        exprval = self.term()
        while self._accept('WS'):
            pass  # Пропуск пробільних символів

        while self._accept('GROUP1') or self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
                self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or self._accept('GROUP8') or \
                self._accept('GROUP0') or self._accept('GROUP988') or self._accept('PRECIPITATION') or \
                self._accept('GROUP966'):
            op = self.tok.type
            right = self.term()
            exprval = (op, exprval, right)

        return exprval

    def term(self):
        "term ::= factor { ('*'|'/') factor }"

        termval = self.factor()
        while self._accept('WS'):
            pass  # Пропуск пробільних символів

        while self._accept('GROUP1') or self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
                self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or self._accept('GROUP8') or \
                self._accept('GROUP0') or self._accept('GROUP988') or self._accept('PRECIPITATION') or \
                self._accept('GROUP966'):
            op = self.tok.type
            right = self.factor()
            termval = (op, termval, right)

        return termval

    def factor(self):
        'factor ::= NUM | ( expr )'
        if self._accept('WS'):
            pass  # Пропуск пробільних символів

        if self._accept('GROUP1') or self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
                self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or self._accept('GROUP8') or \
                self._accept('GROUP0') or self._accept('GROUP988') or self._accept('PRECIPITATION') or \
                self._accept('GROUP966'):
            return self.tok.value
        else:
            raise SyntaxError('Invalid token: ' + self.nexttok.type)


# Приклад використання
# e = ExpressionTreeBuilder()
# tree = e.parse_expression_tree('42148 23081 10048 20021 30056 42123 83123 00000 98822 00052=')
# print(tree)
