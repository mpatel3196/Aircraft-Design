# Aircaft Conceptual Design, Raymer
# ch: 03
# Weight Estimation Data Tables

# Author : Parth Viradiya
# Update History:
#       - created file, 26-Apr-2019

from math import exp, sqrt
from standard_atmosphere import standard_atmosphere


#---------------------------------------------------------------------------------------------

def empty_weight_fraction(W0, aircraft_type, variable_sweep=False):
    '''
    Calculate the empty weight fraction for the given aircraft.
    We_W0 = A*(W0**C)*Kvs
    where,  We_W0 = empty weight fraction
            A , C = coefficients
            W0 = Max takeoff(gross) weight of the aircraft
            Kvs = variable sweep constant,
                = 1.04 if swept wing, otherwise 1

    Parameters
    ------------
    W0 : postive float, Max takeoff(gross) weight of the aircraft
    aircraft_type : positive int number based on the given option 
                    in table.
                    type of aircraft
    variable_sweep : bool, default = False, no variable sweep
                        True if there is a variable sweep geometry
    
    Return
    --------
    We_W0 : empty weight fraction
    '''

    # Lookup Table of Empty weight fraction Vs W0
    # Index for below dictionary
    index_of_table = {
        1: 'Sailplane unpowered',
        2: 'Sailplane powered',
        3: 'Homebuilt- metal/wood',
        4: 'Homebuilt- composite',
        5: 'General Aviation- single engine',
        6: 'General Aviation- twin engine',
        7: 'Agricultural aircraft',
        8: 'Twin turboprop',
        9: 'Flying boat',
        10:  'Jet trainer',
        11: 'Jet fighter- metal',
        12: 'Jet fighter- composite',
        13: 'Military cargo/bomber',
        14: 'Jet transport',
    }
    # structure :=> { 'type of aircraft' : [A, C] }
    Table = {
        'Sailplane unpowered': [0.86, -0.05],
        'Sailplane powered': [0.91, -0.05],
        'Homebuilt- metal/wood': [1.19, -0.09],
        'Homebuilt- composite': [0.99, -0.09],
        'General Aviation- single engine': [2.36, -0.18],
        'General Aviation- twin engine': [1.51, -0.10],
        'Agricultural aircraft': [0.74, -0.03],
        'Twin turboprop': [0.96, -0.05],
        'Flying boat': [1.09, -0.05],
        'Jet trainer': [1.59, -0.10],
        'Jet fighter- metal': [2.34, -0.13],
        'Jet fighter- composite': [1.34, -0.13],
        'Military cargo/bomber': [0.93, -0.07],
        'Jet transport': [1.02, -0.06],
    }

    # coefficients for empty weight fraction
    A, C = Table[index_of_table[aircraft_type]][0], Table[index_of_table[aircraft_type]][1]

    # variable sweep constant
    if variable_sweep:
        Kvs = 1.04  # variable sweep
    else:
        Kvs = 1.00  # fixed sweep

    # empty weight fraction
    We_W0 = A * (W0**C)*Kvs

    return We_W0

#---------------------------------------------------------------------------------------------

def get_empty_weight(W0, We_W0):
    '''
    returns empty weight of aircraft in lbs.
    '''
    W_empty = We_W0 * W0
    return W_empty

# def get_empty_weight(W0, aircraft_type, variable_sweep=False):
#     '''
#     returns empty weight of aircraft in lbs.
#     '''
#     We_W0 = empty_weight_fraction(W0, aircraft_type, variable_sweep=False)
#     W_empty = We_W0 * W0
#     return W_empty

#---------------------------------------------------------------------------------------------

index_mission = {
    1: 'takeoff',
    2: 'climb',
    3: 'cruise',
    4: 'descent',
    5: 'loiter',
    6: 'landing'
}

mission_plan = [1, 2, 3, 4, 5, 4, 6]

#----------------
# different idea

M_cruise = 0.78   # service ceiling, cruise Mach
M_max = 0.82    # speed ceiling, max Mach

cruise_altitude = 42000 # ft
runway_dist = 9000 # ft, take_off_distance == landing_distance

# getting values of temperature and density at cruise_altitude
rho, temp = standard_atmosphere(cruise_altitude)

c = 0.45    # specific fuel consumption, (lb/hour)/lb  # Table[3.3]
V = (M_cruise*39*sqrt(temp)) * 1.687378    # True air speed, V, ft/s,  1.687377 = convert m/s into ft/sec

L_by_D_max = 18  # max L/D ratio
L_by_D_cruise = L_by_D_max * 0.866  # L_by_D_cruise at cruise it is not max

R1 = 2500 # NM, nautical miles, # cruise range based on the mission profile
R1 = R1 * 6074.56    # ft,   6074.56 = conersion factor
R2 = 800 # NM, nautical miles,  # return cruise range based on the mission profile
R2 = R2 * 6074.56    # ft,   6074.56 = conersion factor
E = 15 #* 60  # Loiter Endurance , 15 min , converted to seconds

mission_planning = {
    'takeoff': [],
    'climb': [],
    'cruise': {'Range(ft)': R1, 'True_air_speed(ft/s)': V, 'L_by_D_max': L_by_D_max, 'SFC': c},
    'descent': [],
    'loiter': {'Endurance(minutes)': E, 'L_by_D_max': L_by_D_max, 'SFC': c},
    'climb': [],
    'cruise2': {'Range(ft)': R2, 'True_air_speed(ft/s)': V, 'L_by_D_max': L_by_D_max, 'SFC': c},
    'loiter2': {'Endurance(minutes)': E, 'L_by_D_max': L_by_D_max, 'SFC': c},
    'landing': []
}
#----------------

# book page 27 example :  Test to see accuracy , book_answer = 0.635, this function answer = 0.6347 (PREFECT MATCH)
mission_planning2 = {
    'takeoff': [],
    'climb': [],
    'cruise': {'Range(ft)': 9114000, 'True_air_speed(ft/s)': 569.9, 'L_by_D_max': 16, 'SFC': 0.5},
    'loiter': {'Endurance(minutes)': 180, 'L_by_D_max': 16, 'SFC': 0.4},
    'cruise2': {'Range(ft)': 9114000, 'True_air_speed(ft/s)': 569.9, 'L_by_D_max': 16, 'SFC': 0.5},
    'loiter2': {'Endurance(minutes)': 20, 'L_by_D_max': 16, 'SFC': 0.4},
    'landing': []
}

def mission_profile(mission_planning):
    '''
    Mission Profile Builder.

    '''

    # W0 to W(n) = len(mission_plan) + 1
    n = len(mission_planning) + 1

    # mission segments weight fractions
    if 'takeoff' in mission_planning.keys():
        takeoff_fraction = 0.970
        mission_planning['takeoff'] = takeoff_fraction
    if 'climb' in mission_planning.keys():
        climb_fraction = 0.985
        mission_planning['climb'] = climb_fraction
    if 'descent' in mission_planning.keys():
        descent_fraction = 0.995
        mission_planning['descent'] = descent_fraction
    if 'landing' in mission_planning.keys():
        landing_fraction = 0.995
        mission_planning['landing'] = landing_fraction

    # maybe use looping for multiple cruise and loiters as both range and endurance may differ

    # count haw many cruises are in mission1 planning
    count_cruises = []
    for i in mission_planning.keys():
        if i[:6] == 'cruise':
            count_cruises.append(i)
    
    # count haw many loiter are in mission planning
    count_loiters = []
    for i in mission_planning.keys():
        if i[:6] == 'loiter':
            count_loiters.append(i)

    # cruises mission segments
    cruise_fraction_list = []
    for i in count_cruises:
        Range = mission_planning[i]['Range(ft)']
        TAS = mission_planning[i]['True_air_speed(ft/s)']
        L_by_D_max = mission_planning[i]['L_by_D_max']
        L_by_D_cruise = 0.866 * L_by_D_max     # L/D cruise = 0.866 * L/D max
        SFC = mission_planning[i]['SFC']   # SFC = specific fuel consumption
        cruise_fraction_list.append(exp((-Range*SFC) / (TAS*L_by_D_cruise*3600)))
    cruise_list = ['cruise', 'cruise2', 'cruise3', 'cruise4', 'cruise5']
    for i, k in zip(cruise_list, cruise_fraction_list):
        mission_planning[i] = k

    # loiters mission segments
    loiter_fraction_list = []
    for i in count_loiters:
        Endurance = mission_planning[i]['Endurance(minutes)']*60  # in sec
        SFC = mission_planning[i]['SFC']
        loiter_fraction_list.append(exp((-Endurance*SFC) / (L_by_D_max*3600)))
    loiter_list = ['loiter', 'loiter2', 'loiter3', 'loiter4', 'loiter5']
    for i, k in zip(loiter_list, loiter_fraction_list):
        mission_planning[i] = k

    # calcauating W0_Wn = multiplying all the mission segmenets
    W0_Wn = 1
    for i in mission_planning.keys():
        W0_Wn *= mission_planning[i]
        print(mission_planning[i])
    return W0_Wn


print(mission_profile(mission_planning2))
print(mission_profile(mission_planning))   # still accuracy issue over this case 
                                           # check it for different examples 
