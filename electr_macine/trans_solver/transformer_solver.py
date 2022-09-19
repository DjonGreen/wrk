def trans_two_win_solver(S, U_gs_lin, U_cs_lin, f, m, SHGS, SHCS, Pxx, Ixx, Pk, Uk):
    """Расчет параметров схемы замещения двухобмоточного трансформатора
    Args:
        S ([type]): Мощность сетевой обмотки трансформатора [ВА]
        U_gs_lin ([type]): Номинальное напряжение сетевой обмотки [В]
        U_cs_lin ([type]): Номинальное напряжение вентильной обмотки [В]
        f ([type]): Частота сети [Гц]
        m ([type]): Количество фаз
        SHVN ([type]): Схема соединений сетевой обмотки [D / Y]
        SHNN ([type]): Схема соединений вентильной обмотки [D / Y]
        Pxx ([type]): Потери холостого хода [Вт]
        Ixx ([type]): Ток холостого хода [%]
        Pk ([type]): Потери короткого замыкания [Вт]
        Uk ([type]): Напряжение короткого замыкания [%]

    Returns:
        [type]: [description]
    """
    from math import pi

    # Расчет тока и напряжений СО
    if SHGS == 'D' or SHGS == 'Y' or SHGS == '1':
        if SHGS == 'D':
            I_gs_lin = S / (U_gs_lin * 3**0.5)
            I_gs_ph = I_gs_lin / 3**0.5
            U_gs_ph = U_gs_lin                    #
        elif SHGS == 'Y':
            I_gs_lin = S / (U_gs_lin * 3**0.5)
            I_gs_ph = I_gs_lin   
            U_gs_ph = U_gs_lin / 3**0.5
        elif SHGS == '1':
            I_gs_lin = S / (U_gs_lin)
            I_gs_ph = I_gs_lin   
            U_gs_ph = U_gs_lin
    else: 
        print('Неверный ввод схемы соединения. Введите Y или D.')
    
    # Расчет тока и напряжений ВО1
    if SHCS == 'D' or SHCS == 'Y' or SHCS == '1':
        if SHCS == 'D':
            U_cs_lin = U_cs_lin 
            I_cs_lin = S / (U_cs_lin * 3**0.5)
            I_cs_ph = I_cs_lin / 3**0.5
            U_cs_ph = U_cs_lin                    #
        
        elif SHCS == 'Y':
            U_cs_lin = U_cs_lin 
            I_cs_lin = S / (U_cs_lin * 3**0.5)
            I_cs_ph = I_cs_lin   
            U_cs_ph = U_cs_lin / 3**0.5
        elif SHGS == '1':
            U_cs_lin = U_cs_lin 
            I_cs_lin = S / (U_cs_lin)
            I_cs_ph = I_cs_lin   
            U_cs_ph = U_cs_lin
        
    else: 
        print('Неверный ввод схемы соединения. Введите Y или D.')

    # Вычисление сопротивлений и индуктивностей
    Ixx_ie = I_gs_lin * (Ixx / 100)
    Zm = U_gs_lin / (Ixx_ie * 3**0.5)
    Rm = Pxx / (m * Ixx_ie**2)
    Lm = abs(((((Zm) ** 2) - Rm ** 2)**0.5) / (2 * pi * f))
    Rk = Pk / (m * I_gs_lin**2)
    Zk = Uk * U_gs_lin / (100 * I_gs_lin * 3**0.5 )
    R1 = Rk / 2
    L1 = abs(((Zk)**2 - (2 * R1)**2)**0.5) / (4 * pi * f)
    
    # Проверка схемы соединений СО
    if SHCS == 'D':
        U_cs_ph = U_cs_lin
        I_cs_lin = S / (U_cs_lin * 3**0.5)
        I_сs_ph = I_cs_lin / 3**0.5
        
    if SHCS == 'Y':
        U_cs_ph = U_cs_lin / 3**0.5
        I_cs_ph = S / (U_cs_lin * 3**0.5)
        I_cs_lin = I_cs_ph

    R2 = R1 / ((U_gs_ph / U_cs_ph)**2)
    L2 = L1 / ((U_gs_ph / U_cs_ph)**2)

    print(  f'\n################################'
            f'\nПараметры Трансформатора {S / 1000} кВА, {U_gs_lin}/{U_cs_lin} В, {SHGS}/{SHCS}\n'
            f'\nЛинейный ток обмотки {U_gs_lin} В, I1лин = {I_gs_lin:.2f} А'
            f'\nЛинейный ток обмотки {U_cs_lin} В, I2лин = {I_cs_lin:.2f} А\n'
            f'\nАктивное сопротивление магнитной цепи, Rm = {Rm:.3f} Ом'
            f'\nИндуктивность намагничивания, Lm = {Lm:.3f} Гн\n'
            f'\nАктивное сопротивление обмотки {U_gs_lin} В, R1 = {R1:.3f} Ом'
            f'\nИндуктивность обмотки {U_gs_lin} В, L1 = {L1:.2e} Гн\n'
            f'\nАктивное сопротивление обмотки {U_cs_lin} В, R2 = {R2:.2e} Ом'
            f'\nИндуктивность обмотки {U_cs_lin} В, L2 = {L2:.2e} Гн\n'
            f'\n################################'
            )

def trans_three_win_solver(S, U_gs_lin, U_cs_lin, f, m, SHGS, SHCS_1, SHCS_2 , Pxx, Ixx, Pk, Ukv, Ukv_1, Ukv_2):
    """Расчет параметров Т-схемы замещения трёхобмоточного трансформатора

    Args:
        S (_type_): Номинальная мощность трансформатора
        U_gs_lin (_type_): Номинальное линейное напряжение СО
        U_cs_lin (_type_): Номинальное линейное напряжение ВО1 и ВО2
        f (_type_): Номинальная частота
        m (_type_): Количество фаз
        SHGS (_type_): Схема соединения СО
        SHCS_1 (_type_): Схема соединения ВО1
        SHCS_2 (_type_): Схема соединения ВО2
        Pxx (_type_): Потери холостого хода
        Ixx (_type_): Ток холостого хода
        Pk (_type_): Потери короткого замыкания
        Ukv (_type_): Напряжение короткого замыкания СО
        Ukv_1 (_type_): Напряжение короткого замыкания СО-ВО1
        Ukv_2 (_type_): Напряжение короткого замыкания СО-ВО2
    """
    from math import pi
    # Расчет напряжений короткого замыкания 
    if Ukv_1 != 0 and Ukv_2 != 0:
        Uk1_2 = -2 * Ukv + Ukv_1 + Ukv_2            # Напряжение КЗ ВО1-ВО2
        Uk_1 = (Uk1_2 + Ukv_1 - Ukv_2) / 2          # Напряжение КЗ ВО1
        Uk_2 = (Uk1_2 + Ukv_2 - Ukv_1) / 2          # Напряжение КЗ ВО2
        Uk = (Ukv + Uk_1 + Uk_2) / 3
    else:
        Uk = Ukv
    # Расчет тока и напряжений СО
    if SHGS == 'D' or SHGS == 'Y':
        if SHGS == 'D':
            I_gs_lin = S / (2 * U_gs_lin * 3**0.5)
            I_gs_ph = I_gs_lin / 3**0.5
            U_gs_ph = U_gs_lin                    #
        elif SHGS == 'Y':
            I_gs_lin = S / (2 * U_gs_lin * 3**0.5)
            I_gs_ph = I_gs_lin   
            U_gs_ph = U_gs_lin / 3**0.5
    else: 
        print('Неверный ввод схемы соединения. Введите Y или D.')

    # Расчет тока и напряжений ВО1
    if SHCS_1 == 'D' or SHCS_1 == 'Y':
        if SHCS_1 == 'D':
            U_cs1_lin = U_cs_lin 
            I_cs1_lin = S / (2 * U_cs_lin * 3**0.5)
            I_cs1_ph = I_cs1_lin / 3**0.5
            U_cs1_ph = U_cs_lin                    #
        
        elif SHCS_1 == 'Y':
            U_cs1_lin = U_cs_lin 
            I_cs1_lin = S / (2 * U_cs1_lin * 3**0.5)
            I_cs1_ph = I_cs1_lin   
            U_cs1_ph = U_cs1_lin / 3**0.5
    else: 
        print('Неверный ввод схемы соединения. Введите Y или D.')
        
    # Расчет тока и напряжений ВО2
    if SHCS_2 == 'D' or SHCS_2 == 'Y':
        if SHCS_2 == 'D':
            U_cs2_lin = U_cs_lin 
            I_cs2_lin = S / (2 * U_cs_lin * 3**0.5)
            I_cs2_ph = I_cs2_lin / 3**0.5
            U_cs2_ph = U_cs_lin                    #
        
        elif SHCS_2 == 'Y':
            U_cs2_lin = U_cs_lin 
            I_cs2_lin = S / (2 * U_cs2_lin * 3**0.5)
            I_cs2_ph = I_cs2_lin   
            U_cs2_ph = U_cs2_lin / 3**0.5
    else: 
        print('Неверный ввод схемы соединения. Введите Y или D.')

    # Ток хх, А:
    Ixx_ie = I_gs_lin * (Ixx / 100)
    # Активное сопротивление намагничивающего контура, Ом:
    Rm = Pxx / (m * Ixx_ie**2)
    # Полное сопртивление намагничивающего контура, Ом:
    Zm = U_gs_lin / (Ixx_ie * 3**0.5)
    # Индуктивность магнитной цепи, Гн:
    Lm = abs(((((Zm) ** 2) - Rm ** 2)**0.5) / (2 * pi * f))
    # Активное сопротивление короткого замыкания, Ом:
    Rk = Pk / (m * I_gs_lin**2)
    # Полное сопротивление короткого замыкания, Ом:
    Zk = Uk * U_gs_lin / (100 * I_gs_lin * 3**0.5 )
    # Активное сопротивление СО, Ом:
    R1 = Rk / 2
    # Реальная индуктивность СО, Гн:
    L1 = (((Zk)**2 - (2 * R1)**2)**0.5) / (4 * pi * f)
    # Реальное активное сопротивление ВО1, Ом:
    R2_1 = R1 / ((U_gs_ph / U_cs1_ph)**2)
    # Реальная индуктивность ВО1, Гн:
    L2_1 = L1 / ((U_gs_ph / U_cs1_ph)**2)
    # Реальное активное сопротивление ВО2, Ом:
    R2_2 = R1 / ((U_gs_ph / U_cs2_ph)**2)
    # Реальная индуктивность ВО2, Гн:
    L2_2 = L1 / ((U_gs_ph / U_cs2_ph)**2)

    print(  f'\n################################'
            f'\nПараметры Т-схемы замещения Трансформатора {S / 1000} кВА, {U_gs_lin}/{U_cs_lin}/{U_cs_lin} В, {SHGS}/{SHCS_1}/{SHCS_2}\n'
            f'Линейный ток СО, I1лин = {2 * I_gs_lin:.1f}'
            #f'\nФазный ток СО, I1фаз = {I_gs_ph:.1f}'
            #f'\nФазное напряжение СО, U1фаз = {U_gs_ph:.1f}'
            f'\nЛинейный ток ВО1, I2_1лин = {I_cs1_lin:.1f}'
            #f'\nФазный ток ВО1, I2_1фаз = {I_cs1_ph:.1f}'
            f'\nЛинейный ток ВО2, I2_2лин = {I_cs2_lin:.1f}\n'
            #f'\nФазный ток ВО2, I2_2фаз = {I_cs2_ph:.1f}'
            #f'\nНапряжение КЗ СО {Uk:.2f}'
            #f'\nНапряжение КЗ ВО1 {Uk_1:.2f}'
            #f'\nНапряжение КЗ ВО2 {Uk_2:.2f}'
            #f'\nТок ХХ {Ixx_ie:.2f}'
            f'\nАктивное сопротивление магнитной цепи, Rm = {Rm:.2f}'
            f'\nИндуктивность намагничивания, Lm = {Lm:.3f} Гн\n'
            f'\nАктивное сопротивление СО, R1 = {R1:.2e} Ом'
            f'\nИндуктивность СО обмотки, L1 = {L1:.2e} Гн\n'
            f'\nАктивное сопротивление ВО1 ({SHCS_1}), R2_1 = {R2_1:.2e} Ом'
            f'\nИндуктивность ВО1 ({SHCS_1}), L2_1 = {L2_1:.2e} Гн\n'
            f'\nАктивное сопротивление ВО2 ({SHCS_2}), R2_2 = {R2_2:.2e} Ом'
            f'\nИндуктивность ВО2 ({SHCS_2}), L2_2 = {L2_2:.2e} Гн\n'
            f'\n################################'
            )
    

ols_prech = trans_two_win_solver(2500, 6000, 240, 50, 1, '1', '1', 40, 5, 110, 5.5)
#main_D = transSolver(2000000, 6300, 1950, 50, 3, 'D', 'D', 6500, 0.28, 12000, 7.518)

#main_Y = transSolver(2000000, 6300, 1950, 50, 3, 'D', 'Y', 6500, 0.28, 12150, 7.514)

#prech_100_kVA_1 = trans_two_win_solver(100000, 6300, 420, 50, 3, 'D', 'Y', 390, 0.9, 2000, 3.5)
#prech_100_kVA_2 = trans_two_win_solver(100000, 400, 2000, 50, 3, 'Y', 'D', 390, 0.9, 2000, 3.5)
#prech_100_kVA_3 = trans_two_win_solver(25000, 6300, 1950, 50, 3, 'D', 'D', 150, 2, 1500, 8.5)
# prech_2500_kVA_1 = trans_two_win_solver(2500e3, 6300, 400, 50, 3, 'D', 'Y', 3100, 0.3, 18000, 6)



# prech_15_kVA_1 = trans_two_win_solver(15000, 400, 1850, 50, 3, 'Y', 'D', 91, 3.46, 538, 8.32)
#prech_15_kVA_2 = trans_two_win_solver(15000, 6000, 400, 50, 3, 'D', 'Y', 91, 3.46, 538, 8.32)
#prech_15_kVA_3 = trans_two_win_solver(15000, 400, 2100, 50, 3, 'Y', 'D', 91, 3.46, 538, 8.32)
#prech_10_kVA_1 = trans_two_win_solver(10000, 400, 2050, 50, 3, 'Y', 'D', 91, 3.46, 250, 8.32)
#prech_15_kVA_4 = trans_two_win_solver(15000, 6300, 1950, 50, 3, 'D', 'D', 91, 3.46, 538, 8.32)
#prech_16_kVA_1 = trans_two_win_solver(16000, 400, 2100, 50, 3, 'Y', 'D', 140, 4.8, 310, 4.1)
#prech_Y = transSolver(100000, 400, 2000, 50, 3, 'Y', 'Y', 380, 2.2, 2250, 4.5)
#prech_43_kVA_1 = trans_two_win_solver(43000, 6300, 400, 50, 3, 'Y', 'Y', 390, 0.9, 2000, 4)



#trans_6300 = trans_three_win_solver(6300e3, 6000, 1856, 50, 3, 'Y', 'D', 'Y', 7350, 0.18, 42811, 8.67, 19.38, 21.82)
#trans_4000 = trans_three_win_solver(4000e3, 6300, 1950, 50, 3, 'D', 'D', 'Y', 6500, 0.28, 12000, 7.5, 19.38, 21.82)
#trans_4000_2 = trans_three_win_solver(4000e3, 6300, 1950, 50, 3, 'D', 'D', 'Y', 9100, 0.5, 21000, 6, 0, 0)
#trans_4000_new = trans_three_win_solver(4000e3, 6000, 1950, 50, 3, 'D', 'D', 'Y', 5600, 0.6, 22000, 8, 0, 0)


def time_overcurrent(i_s, i_i2t, t_i2t, k_i2t):
    """ Расчетное время срабатывания защиты от перегрузки

    Args:
        i_s (_type_): текущее действующее значение тока фазы статора двигателя
        i_i2t (_type_): пороговое значение тока фазы статора двигателя, 
                        соответствующее уставке времятоковой защиты I2T
        t_i2t (_type_): нормированное время действия перегрузки
        k_i2t (_type_): нормированная кратность перегрузки
    """
    from math import log
    k = i_s / i_i2t
    t = t_i2t / log((k_i2t**2) / (k_i2t**2 - 1))
    t_oc = t * log((k**2) / (k**2 - 1))
    print(t_oc)
    return t_oc

# time_overcurrent(660*1.81, 660*1.8, 10, 1.8)