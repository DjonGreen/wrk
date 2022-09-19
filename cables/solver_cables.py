
# from over_voltage import over_voltage
from math import pi
import re

CROSS_SECTIONS = [  '50', 
                    '70', 
                    '95', 
                    '120',
                    ] 
# Емкость кабеля ПвВ 3ф. 6 кВ, мкФ/км
CAPACITANCES = {#'70': 0.66,             
                #'95': 0.74, 
                #'120': 0.81,
                '50': 0.292,
                '70': 0.331,
                '95': 0.38,
                '120': 0.418,
                }          
# Индуктивное сопротивление трехжильного кабеля ПвВ 3ф. 6 кВ, Ом/км
X_INDUCTANCE = {'50': 0.098,
                '70': 0.093,
                '95': 0.087,
                '120': 0.084,
                }  
# Индуктивность  трехжильного кабеля ПвВ 3ф. 6 кВ, мГн/км
INDUCTANCE = {  '50': 0.313,
                '70': 0.295,
                '95': 0.278,
                '120': 0.268,
                }  
# Удельное сопротивление Ом/км для медных кабелей 5-го класса гибкости при плюс 20 град С, луженые ГОСТ 22483-77
# Удельное сопротивление для медного трехжильного кабеля ПвВ 3ф. 6 кВ, Ом/км
RESISTANSES= { #'95': 0.210, 
                    #'120': 0.164,
                    '50': 0.387,
                    '70': 0.268,
                    '95': 0.193,
                    '120': 0.153,
                    }  

# Длительные допустимые токи ПвВ 3ф. с общим экраном и оплеткой, А
LONG_CURRENTS = {   #'95': 305, 
                    #'120': 350,
                    '50': 192,
                    '70': 233,
                    '95': 279,
                    '120': 316,                    
                    }    
# Наружные диаметры кабеля ПвВ 3ф. 6 кВ , мм2
DIAMETERS = {
                '50': 47.2,
                '70': 50.4,
                '95': 54.2,
                '120': 57.6,    
            }

# Количество кабелей
NUMBER_OF_CABLES = [6, 10, 12]

# Длина кабелей в км
LENGTH = 0.040           


# Допустимый ток односекундного короткого замыкания кабеля, кА   
SHORT_CURRENTS = {  '95': 11.8, 
                    '120': 14.8,
                    }
# Поправочный коэффициент при температуре среды 50 °С
TEMP_COEFF = 0.73                           


def numbers_of_cables(CROSS_SECTIONS, LONG_CURRENTS, TEMP_COEFF, current_nom):
    """ Функция для расчета количества параллельных кабельных линий
        по длительно допустимому току при 25 град.C
    Args:
        CROSS_SECTIONS (_list_): Список выбранных сечений кабеля
        LONG_CURRENTS (_dict_): Словарь допустимых токов
        TEMP_COEFF (_float_): Поправочный коэффициент при температуре среды 50 °С
        current_nom (_float_): Номинальный ток
    Returns:
        _dict_: Словарь рекомендуемого количества кабелей       
    """
    n = []
    current_max = current_nom * 3.2 * 0.73
    #print(f'Номинальный ток {current_nom} | Максимальный ток {current_max} А')
    for cross in CROSS_SECTIONS:
        quant = round(current_max / (LONG_CURRENTS[cross] * TEMP_COEFF * 1.17))
        #print(f'Сечение {cross} мм2 | Количество {quant}')
        n.append(quant)
    return dict(zip(CROSS_SECTIONS, n))
        

def simple_line_drop(CROSS_SECTIONS, RESISTANSES, INDUCTANCE, current_nom, f_hz, l, LONG_CURRENTS, TEMP_COEFF, r0=0, l0=0, c0=0,  u1=0, p2=0, q2=0):
    """ Падение напряжения при одной ветке кабеля при номинальном токе

    Args:
        CROSS_SECTIONS (_type_): _description_
        RESISTANSES (_type_): _description_
        INDUCTANCE (_type_): _description_
        current_nom (_type_): _description_
        f_hz (_type_): _description_
        l (_type_): _description_
        LONG_CURRENTS (_type_): _description_
        TEMP_COEFF (_type_): _description_
        r0 (int, optional): _description_. Defaults to 0.
        l0 (int, optional): _description_. Defaults to 0.
        c0 (int, optional): _description_. Defaults to 0.
        u1 (int, optional): _description_. Defaults to 0.
        p2 (int, optional): _description_. Defaults to 0.
        q2 (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    from math import pi
    bc = (c0 * 2 * pi * f_hz)
    xl = l0 * 2 * pi * f_hz
    qc12 = 0.5 * u1 * bc
    duu = []
    for cross in CROSS_SECTIONS:
        z_mod = (((RESISTANSES[cross])**2 + ((INDUCTANCE[cross] / 1000) * 2 * pi * f_hz)**2)**0.5)
        du = current_nom * z_mod * (l / 1000)
        #print(f'Сечение {cross} мм2 | Падение напряжения при одном кабеле {du:.1f} В')
        duu.append(round(du, 2))
    return dict(zip(CROSS_SECTIONS, duu))



def curve_radius(CROSS_SECTIONS, DIAMETERS):
    """Расчет допустимого радиуса изгиба кабеля

    Args:
        CROSS_SECTIONS (_type_): Список сечений кабеля
        DIAMETERS (_type_): Словарь диаметров кабеля

    Returns:
        _dict_: Словарь радиусов изгиба
    """
    r = []
    for cross in CROSS_SECTIONS:
        radius = 12 * DIAMETERS[cross]
        #print(f'Сечение {cross} мм2 | Допустимый радиус изгиба {radius:.1f} мм')
        r.append(round(radius, 2))   
    return dict(zip(CROSS_SECTIONS, r))

### Функции печати ###
def print_curve_radius(CROSS_SECTIONS, DIAMETERS, LONG_CURRENTS, TEMP_COEFF, current_nom, f_hz, l, RESISTANSES, INDUCTANCE):
    """ Печать допустимых радиусов изгиба кабелей различных сечений

    Args:
        CROSS_SECTIONS (_type_): _description_
        DIAMETERS (_type_): _description_
    """
    for cross in CROSS_SECTIONS:
        print(f'Сечение {cross} мм^2 | \nДиаметр кабеля {DIAMETERS[cross]} мм | \n'
                f'Допустимый радиус изгиба {curve_radius(CROSS_SECTIONS, DIAMETERS)[cross]:.1f} мм | \n' 
                f'Количество параллельных кабелей {numbers_of_cables(CROSS_SECTIONS, LONG_CURRENTS, TEMP_COEFF, current_nom)[cross]} | \n'
                f'Падение напряжения при {numbers_of_cables(CROSS_SECTIONS, LONG_CURRENTS, TEMP_COEFF, current_nom)[cross]} параллельных ветвей при частоте {f_hz} Гц и длине трассы {l} м: {simple_line_drop(CROSS_SECTIONS, RESISTANSES, INDUCTANCE, current_nom, f_hz, l, LONG_CURRENTS, TEMP_COEFF, r0=0, l0=0, c0=0,  u1=0, p2=0, q2=0)[cross]/ numbers_of_cables(CROSS_SECTIONS, LONG_CURRENTS, TEMP_COEFF, current_nom)[cross]:.2f} В| \n'
                f'Длительный ток при 25 град.С {LONG_CURRENTS[cross]} А \n\n')

#numbers_of_cables(CROSS_SECTIONS, LONG_CURRENTS, TEMP_COEFF, 660)
#print(numbers_of_cables(CROSS_SECTIONS, LONG_CURRENTS, TEMP_COEFF, 660))
#print(curve_radius(CROSS_SECTIONS, DIAMETERS))
#print(simple_line_drop(CROSS_SECTIONS, RESISTANSES, INDUCTANCE, 660 * 2, 18, 40,  LONG_CURRENTS, TEMP_COEFF,))




print_curve_radius(CROSS_SECTIONS, DIAMETERS, LONG_CURRENTS, TEMP_COEFF, 660, 20, 40, RESISTANSES, INDUCTANCE)

# curve_radius()

#
# l = 0.040
# n = 10
# f_hz = 10
# Zo = (INDUCTANCE['120'] * 2 * pi * f_hz / 1000 + RESISTANSES['120']) * l
# im = 1061 * 1.8
# du = im * Zo
# print(du)

# print(CAPACITANCES['120'] * 2 * pi * f_hz * l * n / 1000000) 

