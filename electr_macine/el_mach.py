def torque_spin(p, n):
    """Вычисление момента на валу двигателя

    Args:
        p (float): мощность на валу двигателя в кВт
        n (float): скорость двигателя в об/мин

    Returns:
        float: момент на валу двигателя в кН*м
    """
    return p * 9550 / n

def f_ui(p, n):
    """Вычисление частоты тока и напряжения статора двигателя переменного тока
    Args:
        p (int): количество пар полюсов
        n (float): номинальная синхронная скорость ротора в об/мин

    Returns:
        float: частота тока и напряжения статора
    """
    return (p * n) / 60

print(amg:= torque_spin(6300/2, 180) / 1000)
# print(trid1 := torque_spin(320, 203.42) / 1000, 
#         trid2 := torque_spin(320, 500) / 1000, 
#         trid3 := torque_spin(320, 876) / 1000,
#         trid_max := torque_spin(320, 134) / 1000,
#         sep='\n'
#         )
print(f_ui(5, 150))
def current_motor_nom(S, U_ad, cosphi, kpd_m, kpd_vfd):
    i_ad = S * kpd_vfd / (U_ad * kpd_m * 3 ** 0.5)
    p_ad = S * cosphi * kpd_m / 1000
    print(f'Параметры двигателя  мощностью {S / 1000} кВА \n'
            f'Ток двигателя {i_ad:.1f} А\n'
            f'Мощность на валу {p_ad:.1f} кВт\n'
        )
def vfd_input(p2, u_ad, kpd_m, cosphi_m, kpd_vfd, cosphi_vfd):
    s_out = p2 / (kpd_m * cosphi_m)
    s_in = s_out / (kpd_vfd)
    # p_in = s_in * cosphi_vfd
    i_out = s_out / (u_ad * 3**0.5)
    print(f'Параметры двигателя  мощностью {p2 / 1000} кВт \n'
          f'Полная электрическая мощность двигателя {s_out / 1000:.1f} кВА \n'
          f'Номинальный ток двигателя {i_out:.1f} А \n' 
          f'Полная входная мощность ПЧ {s_in / 1000:.1f} кВА\n'
          #f'Активная входная мощность ПЧ {p_in / 1000:.1f} кВт\n'
            )


def vfd_input_2(p2, s_vfd_out, u_ad, cosphi_m, kpd_m, kpd_vfd, cosphi_vfd, width):
    """_summary_
    Args:
        p2 (_type_): Мощность на валу двигателя в Вт
        s_vfd_out (_type_): Полная мощность ПЧ (выходная) в ВА
        u_ad (_type_): Напряжение двигателя
        cosphi_m (_type_): коэффициент мощности двигателя
        kpd_m (_type_): КПД двигателя
        kpd_vfd (_type_): КПД ПЧ
        cosphi_vfd (_type_): Коэффициент мощности ПЧ
        width (_type_): Ширина шкафа
    """

    s_vfd_in = s_vfd_out / (kpd_vfd)    # Полная входная мощность ПЧ
    s_m_in = s_vfd_out          # Полная мощность двигателя
    p_m_in = s_m_in * cosphi_m
    p_m_out = p_m_in * kpd_m
    i_out = s_m_in / (u_ad * 3**0.5)
    print(  f'Полная выходная мощность ПЧ {s_vfd_out / 1000} кВА \n'
            f'Полная входная мощность ПЧ {s_vfd_in / 1000:.1f} кВА\n'
            f'Полная электрическая мощность двигателя {s_m_in / 1000:.1f} кВА\n'
            f'Активная электрическая мощность двигателя {p_m_in / 1000:.1f} кВт\n'
            f'Мощность на валу двигателя {p_m_out / 1000:.1f} кВт\n'
            f'Напряжение статора двигателя {u_ad:.0f} В\n'
            f'Номинальный ток двигателя (суммарный) {i_out:.1f} А\n'            
            #f'Активная входная мощность ПЧ {p_in / 1000:.1f} кВт\n'
            )    

# vfd_input(6300e3 / 2, 3300, 0.87, 0.96, 0.95, 0.95)


# f1 = f_ui(5, 150)

# m1 = torque_spin(6.3, 180) * 1.8
# m2 = torque_spin(3.15, 180) * 1.8

# current_motor_nom(3800e3, 3300, 0.89, 0.95, 0.95)
# current_motor_nom(3800e3, 3300, 1, 0.95, 0.96)
def print_power_s():
    for i in range(int(3800e3 / 2), 6000001*4, int(3800e3 / 2)):
        vfd_input_2(6300e3, i, 3300, 1.0, 0.95, 0.95, 0.95, 3200)

print_power_s()
# print(6300 / (0.96 * 0.87 * 2) )
# print((6300e3 / (0.96 * 0.87 * 2)) / (3300 * 3**0.5))

class AsyncMotor(object):
    def __init__(self):
        pass
    pass
