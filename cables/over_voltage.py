def over_voltage(line_L, line_C0, line_L0, t_front, motor_L1, motor_U1, line_n_reflect_max):
    """[summary]

    Args:
        line_L ([type]): [description]
        line_C0 ([type]): [description]
        line_L0 ([type]): [description]
        t_front ([type]): [description]
        motor_L1 ([type]): [description]
        motor_U1 ([type]): [description]
        line_n_reflect_max ([type]): [description]

    Returns:
        [float, float]: [description]
    """
    from math import pi
    line_Z0 = (line_L0 / line_C0)**0.5
    line_V_front = 1 / (line_L0 * line_C0)**0.5
    line_w_front = pi / t_front
    line_Z_out = line_w_front * motor_L1
    line_t_front = line_L / line_V_front
    line_n_reflect = line_n_reflect_max * line_t_front / t_front
    line_lambda = 2 * pi * line_V_front / line_w_front
    line_L_critical = line_lambda / 2
    line_over_voltage = motor_U1 * (1 + line_n_reflect_max)
    print('Критическая длина кабеля =', line_L_critical, 'м')
    print('Перенапряжение в линии =', line_over_voltage, 'В')
    return line_L_critical, line_over_voltage