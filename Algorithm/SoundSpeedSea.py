# 一些海水声速计算的经验公式
# https://gorbatschow.github.io/SonarDocs/sound_speed_sea_coppens.en/#


def sound_speed_sea_coppens(T, S, D):
    """
    Coppens 海水声速经验公式\n
    Coppens, Alan B, "Simple equations for the speed of sound in Neptunian waters", 1981
    :param T: 温度 (degree Celsius, -2 < T < 35)
    :param S: 盐度 (ppt, 0 < S < 42)
    :param D: 深度 (m, 0 < D < 4000)
    :return: 海水声速 (m/s)
    """
    d = D * 1e-3
    t = T * 1e-1

    C = 1449.05 + 45.7 * t - 5.21 * (t ** 2) + 0.23 * t ** 3 \
        + (1.333 - 0.126 * t + 0.009 * (t ** 2)) * (S - 35) \
        + (16.23 + 0.253 * t) * d + (0.213 - 0.1 * t) * (d ** 2) \
        + (0.016 + 0.0002 * (S - 35)) * (S - 35) * t * d
    return C


def sound_speed_sea_mackenzie(T, S, D):
    """
    Mackenzie 海水声速经验公式\n
    Mackenzie, Kenneth V, "Nine‐term equation for sound speed in the oceans", 1981
    :param T: 温度 (degree Celsius, -2 < T < 30)
    :param S: 盐度 (ppt, 25 < S < 40)
    :param D: 深度 (m, 0 < D < 8000)
    :return: 海水声速 (m/s)
    """
    C = 1448.96 + 4.591 * T - 5.304e-2 * (T ** 2) + 2.374e-4 * (T ** 3) \
        + 1.340 * (S - 35) + 1.630e-2 * D + 1.675e-7 * (D ** 2) \
        - 1.025e-2 * T * (S - 35) - 7.139e-13 * T * (D ** 3)
    return C


def sound_speed_sea_delgrosso(T, S, P):
    """
    Del Grosso 海水声速经验公式\n
    Del Grosso, Vincent A, "New equation for the speed of sound in natural waters (with comparisons to other equations)", 1974\n
    Wong, George SK; Zhu, Shi‐ming, "Speed of sound in seawater as a function of salinity, temperature, and pressure", 1995
    :param T: 温度 (degree Celsius, 0 < T < 35)
    :param S: 盐度 (ppt, 29 < S < 43)
    :param P: 压强 (kPa, 0 < P < 98000)
    :return: 海水声速 (m/s)
    """
    C000 = 1402.392
    CT1 = 0.5012285e1
    CT2 = -0.551184e-1
    CT3 = 0.221649e-3
    CS1 = 0.1329530e1
    CS2 = 0.1288598e-3
    CP1 = 0.1560592
    CP2 = 0.2449993e-4
    CP3 = -0.8833959e-8
    CST = -0.1275936e-1
    CTP = 0.6353509e-2
    CT2P2 = 0.2656174e-7
    CTP2 = -0.1593895e-5
    CTP3 = 0.5222483e-9
    CT3P = -0.4383615e-6
    CS2P2 = -0.1616745e-8
    CST2 = 0.9688441e-4
    CS2TP = 0.4857614e-5
    CSTP = -0.3406824e-3

    p = P * 1.019716e-2

    CT = CT1 * T + CT2 * (T ** 2) + CT3 * (T ** 3)
    CS = CS1 * S + CS2 * (S ** 2)
    CP = CP1 * p + CP2 * (p ** 2) + CP3 * (p ** 3)
    CSTP = CTP * T * p + CT3P * (T ** 3) * p + CTP2 * T * (p ** 2) + \
           CT2P2 * (T ** 2) * (p ** 2) + CTP3 * T * (p ** 3) + \
           CST * S * T + CST2 * S * (T ** 2) + CSTP * S * T * p + \
           CS2TP * (S ** 2) * T * p + CS2P2 * (S ** 2) * (p ** 2)

    C = C000 + CT + CS + CP + CSTP

    return C


def sound_speed_sea_unesco(T, S, P):
    """
    UNESCO 海水声速经验公式\n
    Chen, Chen‐Tung; Millero, Frank J, "Speed of sound in seawater at high pressures", 1977\n
    Millero, FJ; Li, X, "On equations for the speed of sound in seawater-comment", 1994
    :param T: 温度 (degree Celsius, 0 < T < 40)
    :param S: 盐度 (ppt, 5 < S < 40)
    :param P: 压强 (kPa, 0 < P < 100000)
    :return: 海水声速 (m/s)
    """
    C00 = 1402.388
    C01 = 5.03830
    C02 = -5.81090e-2
    C03 = 3.3432e-4
    C04 = -1.47797e-6
    C05 = 3.1419e-9
    C10 = 0.153563
    C11 = 6.8999e-4
    C12 = -8.1829e-6
    C13 = 1.3632e-7
    C14 = -6.1260e-10
    C20 = 3.1260e-5
    C21 = -1.7111e-6
    C22 = 2.5986e-8
    C23 = -2.5353e-10
    C24 = 1.0415e-12
    C30 = -9.7729e-9
    C31 = 3.8513e-10
    C32 = -2.3654e-12
    A00 = 1.389
    A01 = -1.262e-2
    A02 = 7.166e-5
    A03 = 2.008e-6
    A04 = -3.21e-8
    A10 = 9.4742e-5
    A11 = -1.2583e-5
    A12 = -6.4928e-8
    A13 = 1.0515e-8
    A14 = -2.0142e-10
    A20 = -3.9064e-7
    A21 = 9.1061e-9
    A22 = -1.6009e-10
    A23 = 7.994e-12
    A30 = 1.100e-10
    A31 = 6.651e-12
    A32 = -3.391e-13
    B00 = -1.922e-2
    B01 = -4.42e-5
    B10 = 7.3637e-5
    B11 = 1.7950e-7
    D00 = 1.727e-3
    D10 = -7.9836e-6

    p = P * 1e-2

    Cw = (C00 + C01 * T + C02 * (T ** 2) + C03 * (T ** 3) + C04 * (T ** 4) + C05 * (T ** 5)) \
         + (C10 + C11 * T + C12 * (T ** 2) + C13 * (T ** 3) + C14 * (T ** 4)) * p \
         + (C20 + C21 * T + C22 * (T ** 2) + C23 * (T ** 3) + C24 * (T ** 4)) * (p ** 2) \
         + (C30 + C31 * T + C32 * (T ** 2)) * (p ** 3)

    A = (A00 + A01 * T + A02 * (T ** 2) + A03 * (T ** 3) + A04 * (T ** 4)) \
        + (A10 + A11 * T + A12 * (T ** 2) + A13 * (T ** 3) + A14 * (T ** 4)) * p \
        + (A20 + A21 * T + A22 * (T ** 2) + A23 * (T ** 3)) * (p ** 2) \
        + (A30 + A31 * T + A32 * (T ** 2)) * (p ** 3)

    B = B00 + B01 * T + (B10 + B11 * T) * p

    D = D00 + (D10 * p)

    C = Cw + A * S + B * (S ** (3 / 2)) + D * (S ** 2)

    return C


def sound_speed_sea_npl(T, S, D, L):
    """
    NPL 海水声速经验公式\n
    Leroy, Claude C; Robinson, Stephen P; Goldsmith, Mike J, "A new equation for the accurate calculation of sound speed in all oceans", 2008
    :param T: 温度 (degree Celsius, -1 < T < 30)
    :param S: 盐度 (ppt, 0 < S < 42)
    :param D: 深度 (m, 0 < D < 12000)
    :param L: 纬度 (degree, -90 < L < 90)
    :return: 海水声速 (m/s)
    """
    C = 1402.5 + 5 * T - 5.44e-2 * (T ** 2) + 2.1e-4 * (T ** 3) \
        + 1.33 * S - 1.23e-2 * S * T + 8.7e-5 * S * (T ** 2) \
        + 1.56e-2 * D + 2.55e-7 * (D ** 2) - 7.3e-12 * (D ** 3) \
        + 1.2e-6 * D * (L - 45) - 9.5e-13 * T * (D ** 3) + 3e-7 * (T ** 2) * D \
        + 1.43e-5 * S * D
    return C
