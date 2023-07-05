import collections
import re

    # def parse(self):
    #     self.current_token = None
    #     self.next_token = None

    #     parsed_telegram = {
    #         'date_telegram': '',
    #         'time_telegram': '',
    #         'index_station': '',
    #         'gauges_telegram': {}
    #     }

    #     self.advance()  # Перенесено перед викликом expr()

    #     parsed_telegram['date_telegram'] = self.expr('DATE')
    #     parsed_telegram['time_telegram'] = self.expr('TIME')
    #     parsed_telegram['index_station'] = self.expr('INDEX')

    #     # Обробка розділів
    #     while self.current_token is not None:
    #         section = self.current_token.type
    #         if section in ['GROUP1', 'GROUP2', 'GROUP3', 'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7', 'GROUP8']:
    #             self.process_section(section, parsed_telegram['gauges_telegram'])
    #         self.advance()

    #     return parsed_telegram


    # def advance(self):
    #     self.current_token = self.next_token
    #     if self.tokens:
    #         self.next_token = self.tokens.pop(0)
    #     else:
    #         self.next_token = None

    # def match(self, expected_type):
    #     if self.current_token.type == expected_type:
    #         self.advance()
    #     else:
    #         raise SyntaxError(f"Expected {expected_type}, but found {self.current_token.type}")
        # def expr(self, expr_type):
    #     if self.current_token is not None and self.current_token.type == expr_type:
    #         value = self.current_token.value
    #         self.advance()
    #         return value
    #     else:
    #         raise SyntaxError(f"Expected {expr_type}, but found {self.current_token.type}")
        # def term(self):
    #     term_value = self.factor()
    #     while self.current_token.type != 'END':
    #         op = self.current_token.type
    #         self.advance()
    #         right = self.factor()
    #         term_value = (op, term_value, right)
    #     return term_value

    # def factor(self):
    #     if self.current_token.type.startswith('GROUP'):
    #         group_type = self.current_token.type
    #         group_value = self.current_token.value
    #         self.advance()
    #         return self.process_group(group_type, group_value)
    #     else:
    #         raise SyntaxError('Invalid token: ' + self.current_token.type)
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

class TelegramParser:
     # # Токенизатор
    Token = collections.namedtuple('Token', ['type', 'value'])

    def __init__(self, **kwargs):
        self.index_station = kwargs['index_station']
        self.date_telegram = kwargs['date_telegram'][8:]
        self.time_telegram = kwargs['time_telegram'][:2]
        self.gauges_telegram = kwargs['gauges_telegram']
        self.d = self.date_telegram+self.time_telegram
        self.INDEX = r'(?P<INDEX>{})'.format(self.index_station)
        self.DATE_TIME = r'(?P<DATE_TIME>{}/d)'.format(self.d)
        self.WS = r'(?P<WS>\s+)'
        self.GROUP1 = r'(?P<GROUP1>1\d+)'
        self.GROUP2 = r'(?P<GROUP2>2\d+)'
        self.GROUP3 = r'(?P<GROUP3>3\d{4})'
        self.GROUP4 = r'(?P<GROUP4>4\d{4}|4\d{2}//|4////)'
        self.GROUP5 = r'(?P<GROUP5>5\d{4})'
        self.GROUP6 = r'(?P<GROUP6>6\d{4}|6\d{5})'
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
        # self.tokens = [x for x in self.generate_tokens()] 
        self.tokens = self.generate_tokens()
        self.tok = None
        self.nexttok = None
        
 
    def generate_tokens(self):
        scanner = self.master_pat.scanner(self.gauges_telegram)
        for m in iter(scanner.match, None):
            tok = self.Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok




    def parse(self):
        
        self._advance()  # Додайте цей рядок
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


          
    def factor(self):
        if self._accept('WS'):
            pass  # Пропуск пробільних символів
        if self.nexttok is None:
            # Check if next token exists
            return None

        if self._accept('INDEX') or self._accept('DATE_TIME') or self._accept('GROUP1') or \
            self._accept('GROUP2') or self._accept('GROUP3') or self._accept('GROUP4') or \
            self._accept('GROUP5') or self._accept('GROUP6') or self._accept('GROUP7') or \
            self._accept('GROUP8') or \
            self._accept('GROUP0') or self._accept('GROUP988') or \
            self._accept('GROUP966') or self._accept('END'): 
            return self.tok.value
        else:
            raise SyntaxError('Invalid token: ' + (self.nexttok.type if self.nexttok else 'None'))

    def process_section(self, section, gauges_telegram):
        # Обробка кожного розділу окремо
        if section == 'GROUP1':
            group_type = section
            group_value = self.current_token.value
            self.advance()
            self.process_group1(group_type, group_value, gauges_telegram)
        # Додайте обробку інших розділів за необхідності

    def process_group1(self, group_type, group_value, gauges_telegram):
        # Обробка групи 1 за вашою логікою
        pass
        # Збережіть дані групи у відповідних змінних або об'єктах

    # Додайте інші методи обробки груп, які вам потрібні

# Приклад використання
d ={'date_telegram': '2023-06-05', 
    'time_telegram': '08:00:00', 
    'index_station': '42187',
    'gauges_telegram': '42187 04081 10054 20052 30058 82166 00000 98803 00000 96606 11223 23555 34555 46666 55555 66666 77777 88888 99999='}
    
s = TelegramParser(**d)
s.parse()
print([x for x in s.generate_tokens()])
print(s.parse())