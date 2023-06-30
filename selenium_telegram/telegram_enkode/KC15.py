from dataclasses import dataclass
import re

@dataclass
class HydroTelegramData:
    index: str
    date_time_type: str
    group1: str
    group2: str
    group3: str
    group4: str
    group5: str
    group6: str
    group7: str
    group8: str
    group0: str
    group988: str
    group988_0: str
    group922: str
    group922_1: str
    group922_2: str
    group922_3: str
    group922_4: str
    group922_5: str
    group922_6: str
    group922_7: str
    group922_8: str
    

    # і так далі для інших груп параметрів
    
    def __init__(self, telegram):
        self.parse_telegram(telegram)
    
    def parse_telegram(self, telegram):
        token_patterns = {
            'index': r'\d{5}',
            'date_time': r'\d{2}\d{2}',
            'group1': r'\d{5}',
            'group2': r'\d{5}',
            # і так далі для інших груп параметрів
        }
        
        for token_name, pattern in token_patterns.items():
            match = re.search(pattern, telegram)
            if match:
                setattr(self, token_name, match.group(0))
            else:
                setattr(self, token_name, None)



class IndexParser:
    def process_value(self, value):
        # Логіка обробки для індексу поста
        return value

class DateParser:
    def process_value(self, value):
        # Логіка обробки для дати
        return  value

class TimeParser:
    def process_value(self, value):
        # Логіка обробки для часу
        return value
    
class TypeParser:
      def process_value(self, value):
        # Логіка обробки для часу
        return value[-1]

class group1Parser:
    def process_value(self, value):
        # Логіка обробки для часу
        return value
    
class group2:
    def process_value(self, value):
        # Логіка обробки для часу
        return value

class group3:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group5:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group6:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group7:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group8:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group0:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group988:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    

class group988_0:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    

class group922:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    
class group4:
    def process_value(self, value):
        # Логіка обробки для часу
        return value    


# Створіть інстанси класів згідно потрібного порядку
parsers = [
    IndexParser(),
    DateParser(),
    TimeParser(),
    # Додайте інші класи для решти груп параметрів
]

# Додайте NullValue як останній об'єкт у списку parsers


# Задайте телеграму, яку потрібно розкодувати
telegram = "42187 2023-06-05 08:00:00 10051 20032 30052 82163 00000 98804 00000="

# Розділіть телеграму на окремі елементи
elements = telegram.split()

# Проітеруйтеся по списку parsers та викликайте метод process_value для кожного елемента телеграми
decoded_values = []
for parser, value in zip(parsers, elements):
    decoded_value = parser.process_value(value)
    decoded_values.append(decoded_value)

# Отримані значення зберігаються у списку decoded_values
print(decoded_values)
d ={'date_telegram': '2023-06-05', 
    'time_telegram': '08:00:00', 
    'index_station': '42187',
    'gauges_telegram': '42187 05081 10051 20032 30052 82163 00000 98804 00000='}



  