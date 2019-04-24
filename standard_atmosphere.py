def standard_atmosphere(alt):
    '''
    Calculate the values of Density(Rho) and Temperature(T) for given altitude.
    # standard Atmosphere upto 20KM

    Parameters
    ------------
    alt: altitude, m

    Returns
    ---------
    Rho: density, N/m^2
    T: tempraturre, K
    '''
    #sea level conditions
    Ps=1.01325e5  # in N/m^2
    Rhos= 1.2250  # in kg/m^3
    Ts= 288.16 # in K
    alt_s= 0 # in m

    g0 = 9.8 # m/s^2 graviational constant
    R= 287 # gas constant, # 1716.3 in english unit

    if alt>0 and alt<=11000 : # grandeint Region in standard atmosphere
        a= -6.5e-3 # in Kelvin/metre # Lapse Rate for 0 t 11 Km Altitude
        T = Ts + a*(alt-alt_s)
        Rho = Rhos * ((T/Ts)**-((g0/(a*R))+1))
    elif alt>11000 and alt<20000 :  # isothermal region in standard atmosphere
        Rho_11=0.367 # in kg/m^3 density at 11 KM altitude
        T=216.66 # in K for 11 to 25 KM due to Isothermal region
        alt_11= 11000 # in metre base value for isothermal region 
        Rho = Rho_11 * (exp(-1*(g0/(T*R))*(alt-alt_11)))

    return Rho, T

if __name__=='__main__':
    # getting values from standard atmosphere
    Rho, T = standard_atmosphere(5000)   # 5km
    print(f'Rho = {Rho}')
    print(f'T = {T}')
    