


def precharge(c_dc, r_prech, u_dc, u_ac_lin_input):
    tau_prech = r_prech * c_dc
    time_prech = tau_prech * 5
    u_level = 0.95 * u_ac_lin_input * 2**0.5
    print(time_prech, " сек\n", u_level, " В", sep='')
    return u_dc == u_level


precharge(4 * 10**-3, 300, 5600, 2 * 1950)