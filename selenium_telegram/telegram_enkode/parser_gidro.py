import ply.lex as lex
import ply.yacc as yacc


# Визначення токенів (лексем)
# tokens = (
#     'INDEX',
#     'DATE_TIME',
#     'GROUP1',
#     'GROUP2',
#     'GROUP3',
#     'GROUP4',
#     'GROUP5',
#     'GROUP6',
#     'GROUP7',
#     'GROUP8',
#     'GROUP0',
#     'PRECIPITATION'
#     # 'END'
# )

# # Регулярні вирази для токенів
# t_INDEX = r'\d{5}'
# t_DATE_TIME = r'\d{5}'
# t_GROUP1 = r'1\d{4}'
# t_GROUP2 = r'2\d{4}'
# t_GROUP3 = r'3\d{4}'
# t_GROUP4 = r'4\d{4}|4\d{2}//|4////'
# t_GROUP5 = r'5\d{4}'
# t_GROUP6 = r'6\d{4}'
# t_GROUP7 = r'7\d{4}'
# t_GROUP8 = r'8\d{4}'
# t_GROUP0 = r'0\d{4}|0\d{3}/'
# t_PRECIPITATION = r'988\d+\s0\d{4}|0\d{3}/'


# # t_END = r'='

# # Ігнорувати пробіли та переведення рядка
# t_ignore = ' \n'

# def t_INDEX(t):
#     r'\d{5}'
#     t.value = t.value
#     return t

# def t_DATE_TIME(t):
#     r'\d{5}'
#     t.value = t.value
#     return t

# def t_GROUP1(t):
#     r'1\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP2(t):
#     r'2\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP3(t):
#     r'3\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP4(t):
#     r'4\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP5(t):
#     r'5\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP6(t):
#     r'6\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP7(t):
#     r'7\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP8(t):
#     r'8\d{4}'
#     t.value = t.value
#     return t

# def t_GROUP0(t):
#     r'0\d{4}'
#     t.value = t.value
#     return t

# def t_PRECIPITATION(t):
#     r'988\d+\s\d{5}'
#     t.value = t.value
#     return t

# def t_END(t):
#     r'='
#     return t
tokens = (
    'INDEX',
    'DATE_TIME',
    'GROUP',
    'PRECIPITATION',
)

# Регулярні вирази для токенів
t_INDEX = r'\d{5}'
t_DATE_TIME = r'\d{5}'
t_GROUP = r'\d+|\d{4}\s+|\d{3}\s+|\d{2}\s+\d{1}\s+'
t_PRECIPITATION = r'988\d{2}\s\d+'

# Ігнорувати пробіли та переведення рядка
t_ignore = ' \n'

# Правила граматики
def p_data(p):
    '''
    data : INDEX DATE_TIME groups PRECIPITATION
    '''
    index = p[1]
    date_time = p[2]
    groups = p[3]
    precipitation = p[4]
    
    # Виконати потрібні дії з отриманими даними
    # Наприклад, вивести їх на екран або зберегти у відповідні змінні
    
    print("Index:", index)
    print("Date and Time:", date_time)
    print("Groups:", groups)
    print("Precipitation:", precipitation)

def p_groups(p):
    '''
    groups : group groups
           | group
           | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []
# Функція для обробки синтаксичних помилок
def t_error(t):
    print("Lexical error:", t.value[0])
    t.lexer.skip(1)

# Правила граматики
def p_data(p):
    '''
    data : INDEX DATE_TIME groups PRECIPITATION 
    '''
    index = p[1]
    date_time = p[2]
    groups = p[3]
    precipitation = p[4]

    # Виконати потрібні дії з отриманими даними
    # Наприклад, вивести їх на екран або зберегти у відповідні змінні

    print("Index:", index)
    print("Date and Time:", date_time)
    print("Groups:", groups)
    print("Precipitation:", precipitation)


def p_group(p):
    '''
    group : GROUP
    '''
    p[0] = p[1]

# def p_group(p):
#     '''
#     group : GROUP1
#           | GROUP2
#           | GROUP3
#           | GROUP4
#           | GROUP5
#           | GROUP6
#           | GROUP7
#           | GROUP8
#           | GROUP0
#     '''
#     p[0] = p[1]


# def p_index(p):
#     '''
#     index : INDEX
#     '''
#     index = p[1]

#     # Виконати потрібні дії з отриманим значенням індексу
#     # Наприклад, вивести його на екран або зберегти у відповідну змінну

#     print("Index:", index)

# def p_group4_optional(p):
#     '''
#     group4_optional : empty
#     '''
#     p[0] = None



def p_empty(p):
    '''
    empty :
    '''
    pass

# Функція для обробки синтаксичних помилок
def p_error(p):
    print("Syntax error in input:", p)



# Створення лексера
lexer = lex.lex()

# Створення парсера
parser = yacc.yacc()

# Вхідний текст для розпарсування
input_text = '42148 23081 10048 20021 30056 42123 83123 00000 98822 00000='

# Розпарсування вхідного тексту
parser.parse(input_text)

