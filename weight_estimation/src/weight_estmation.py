# Aircaft Conceptual Design, Raymer
# ch: 03
# Weight Estimation

# Author : Parth Viradiya
# Update History:
#       - 26-Apr-2019 -created
#       - 27-Apr-2019

import sys
sys.path.append('..')
from math import exp, sqrt

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
    aircraft_type : positive int, number based on the given option 
                    in table.
                    type of aircraft
    variable_sweep : bool, default = False, no variable sweep
                        True if there is a variable sweep geometry
    
    Return
    --------
    We_W0 : positive float, empty weight fraction
    '''

    # Lookup Table of Empty weight fraction Vs W0
    # Index for below dictionary
    index_of_table = {
        1: 'Sailplane unpowered',
        2: 'Sailplane powered',
        3: 'Homebuilt- metal/wood',
        4: 'Homebuilt- composite',
        5: 'General Aviation- single engine',
        6: 'General Aviation- single engine',
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
        'General Aviation- single engine': [2.36, -0.18],
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

def get_empty_weight(W0, aircraft_type, variable_sweep=False):
    '''
    returns empty weight of aircraft in lbs.

    Paramters
    ----------
    W0 : postive float, Max takeoff(gross) weight of the aircraft
    aircraft_type : positive int, number based on the given option 
                    in table.
                    type of aircraft
    variable_sweep : bool, default = False, no variable sweep
                        True if there is a variable sweep geometry

    Return
    -------
    W_empty : positive float, empty weight of the aircraft
    '''

    # variable sweep
    if variable_sweep:
        variable_sweep = True
    else:
        variable_sweep=False

    We_W0 = empty_weight_fraction(W0, aircraft_type, variable_sweep=variable_sweep)
    W_empty = We_W0 * W0
    return W_empty

#---------------------------------------------------------------------------------------------

def fuel_weight_fraction(mission_profile, engine_type):
    '''
    Calculate the fuel weight fraction for the given aircraft ..
    .. based on the mission profile.

    Parameters
    ------------
    mission_profile : dict, mission profiile of the aircraft build in ..
                        .. specific way described above.
    engine_type : str, type of engine.
                    choices :   - Pure Turbo Jet
                                - Low-bypass turbofan
                                - High-bypass turbofan
                                - Piston-prop fixed pitch
                                - Piston-prop variable pitch
                                - Turboprop
    
    Return
    --------
    Wf_W0 : positive float, fuel weight fraction
    '''

    # engine choices
    engine_choices = ['Pure Turbo Jet', 'Low-bypass turbofan','High-bypass turbofan', 'Piston-prop fixed pitch', \
                    'Piston-prop variable pitch', 'Turboprop']
    
    # for calcualtion so main dont have to modify mission profile dictionary
    mission_profile_calc = mission_profile.copy()

    # W0 to W(n) = len(mission_plan) + 1
    n = len(mission_profile) + 1

    # mission segments weight fractions
    for i in mission_profile.keys():
        if 'takeoff' == i:
            takeoff_fraction = 0.970
            mission_profile_calc[i] = takeoff_fraction
        if 'climb' == i[:5]:
            climb_fraction = 0.985
            mission_profile_calc[i] = climb_fraction
        if 'descent' == i[:7]:
            descent_fraction = 0.995
            mission_profile_calc[i] = descent_fraction
        if 'landing' == i:
            landing_fraction = 0.995
            mission_profile_calc[i] = landing_fraction

    # count haw many cruises are in mission1 planning
    count_cruises = []
    for i in mission_profile.keys():
        if i[:6] == 'cruise':
            count_cruises.append(i)
    
    # count haw many loiter are in mission planning
    count_loiters = []
    for i in mission_profile.keys():
        if i[:6] == 'loiter':
            count_loiters.append(i)

    # cruises mission segments
    cruise_fraction_list = []
    for i in count_cruises:
        Range = mission_profile[i]['Range(NM)'] * 6074.56  # converting to feet
        TAS = mission_profile[i]['True_air_speed(ft/s)']
        L_by_D_max = mission_profile[i]['L_by_D_max']
        if engine_type in engine_choices[:4]:  # if jet engine
            L_by_D_cruise = 0.866 * L_by_D_max     # L/D cruise = 0.866 * L/D max
        else:   # if prop engine
            L_by_D_cruise = L_by_D_max
        # SFC_cruise, SFC_loiter = get_SFC(engine_type, V)
        SFC_cruise = mission_profile[i]['SFC']   # SFC = specific fuel consumption
        cruise_fraction_list.append(exp((-Range*SFC_cruise) / (TAS*L_by_D_cruise*3600)))
    cruise_list = ['cruise', 'cruise2', 'cruise3', 'cruise4', 'cruise5']
    for i, k in zip(cruise_list, cruise_fraction_list):
        mission_profile_calc[i] = k

    # loiters mission segments
    loiter_fraction_list = []
    for i in count_loiters:
        Endurance = mission_profile[i]['Endurance(minutes)']*60  # in sec
        # _, SFC_loiter =  get_SFC(engine_type, V)
        SFC_loiter = mission_profile[i]['SFC']
        L_by_D_max = mission_profile[i]['L_by_D_max']
        if engine_type in engine_choices[:4]:  # if jet engine
            L_by_D_max = L_by_D_max     # L/D cruise = 0.866 * L/D max
        else:   # if prop engine
            L_by_D_max = L_by_D_max * 0.866
        loiter_fraction_list.append(exp((-Endurance*SFC_loiter) / (L_by_D_max*3600)))
    loiter_list = ['loiter', 'loiter2', 'loiter3', 'loiter4', 'loiter5']
    for i, k in zip(loiter_list, loiter_fraction_list):
        mission_profile_calc[i] = k

    # calcauating Wn_W0 = multiplying all the mission segmenets
    Wn_W0 = 1
    for i in mission_profile_calc.keys():
        Wn_W0 *= mission_profile_calc[i]

    # Fuel weight estimation
    # based on the mission profile
    Wf_W0 = 1.06*(1 - Wn_W0)

    return Wf_W0

#---------------------------------------------------------------------------------------------

def get_fuel_weight(W0, mission_profile, engine_type):
    '''
    returns empty weight of aircraft in lbs.

    Parameters
    ------------
    W0 : postive float, Max takeoff(gross) weight of the aircraft
    mission_profile : dict, mission profiile of the aircraft build in ..
                        .. specific way described above.
    engine_type : str, type of engine.
                    choices :   - Pure Turbo Jet
                                - Low-bypass turbofan
                                - High-bypass turbofan
                                - Piston-prop fixed pitch
                                - Piston-prop variable pitch
                                - Turboprop
    
    Return
    --------
    Wf_W0 : positive float, fuel weight fraction
    '''
    Wf_W0 = fuel_weight_fraction(mission_profile, engine_type)
    W_fuel = Wf_W0 * W0
    return W_fuel

#---------------------------------------------------------------------------------------------

def get_takeoff_gross_weight(W_payload, mission_profile, aircraft_type, engine_type, variable_sweep=False):
    '''
    returns max takeoff weight (gross takeoff weight), lbs.

    Paramters
    ----------
    W_payload : positive flaot, lbs, total payload for the aircraft
    mission_profile : dict, mission profiile of the aircraft build in ..
                        .. specific way described above.
    engine_type : str, type of engine.
                    choices :   - Pure Turbo Jet
                                - Low-bypass turbofan
                                - High-bypass turbofan
                                - Piston-prop fixed pitch
                                - Piston-prop variable pitch
                                - Turboprop
    variable_sweep : bool, default = False, no variable sweep
                    True if there is a variable sweep geometry

   Return
   --------
    W0 : postive float, Max takeoff(gross) weight of the aircraft
    '''

    # checking for correct input of engine type
    engine_choices = ['Pure Turbo Jet', 'Low-bypass turbofan','High-bypass turbofan', 'Piston-prop fixed pitch', \
                    'Piston-prop variable pitch', 'Turboprop']
    assert engine_type in engine_choices, 'Engine Type must be choosen from avilable engine choices'

    # variable sweep
    if variable_sweep:
        variable_sweep = True
    else:
        variable_sweep=False
    
    W0_guess = 5000    # random guess
    We_W0 = empty_weight_fraction(W0_guess, aircraft_type=aircraft_type, variable_sweep=variable_sweep)
    Wf_W0 = fuel_weight_fraction(mission_profile, engine_type)
    W0 = (W_payload) / abs(1 - We_W0 - Wf_W0)
    # while W0_guess != W0 :
    while abs(W0_guess - W0) > 0.000001:
        W0_guess = W0
        # We_W0 = A*(W0_guess**C)
        We_W0 = empty_weight_fraction(W0_guess, aircraft_type=aircraft_type, variable_sweep=variable_sweep)
        W0 = (W_payload)/ abs(1 - We_W0 - Wf_W0)

    return W0

#---------------------------------------------------------------------------------------------

def get_SFC(engine, V):
    '''
    returns the SFC for the cruise and loiter of the given type of engine used in aircraft.
    
    Paramters
    ----------
    engine : str, type of engine
    V : postive float, True Airspeed

    Return
    -------
    C_cruise : positive float, SFC when cruise
    C_loiter : positive float, SFC when loiter
    '''

    # Typical SFC for different engines
    # structure :   { engine_type : [criuseSFC, loiterSFC]}
    # structure :   { engine_type : [criuseSFC, prop_eff, loiterSFC, prop_eff]}
    engines_sfc_table = {
        'Pure turbojet': [0.85, 0.75],
        'Low-bypass turbofan': [0.75, 0.65],
        'High-bypass turbofan': [0.45, 0.35],
        'Piston-prop fixed pitch': [0.4, 0.8 , 0.5, 0.7],
        'Piston-prop variable pitch': [0.4, 0.8 , 0.5, 0.8],
        'Turboprop': [0.5, 0.8 , 0.6, 0.8],
    }

    # calculation for prop engine SFC
    if engine in ['Piston-prop fixed pitch', 'Piston-prop variable pitch', 'Turboprop']:
        C_bhp_cruise = (engines_sfc_table[engine][0]*V) / (550*engines_sfc_table[engine][1])
        C_bhp_loiter = (engines_sfc_table[engine][2]*V) / (550*engines_sfc_table[engine][3])
        C_cruise, C_loiter = C_bhp_cruise, C_bhp_loiter
        return C_cruise, C_loiter
    
    # jet engine SFC calcuation
    C_cruise = engines_sfc_table[engine][0] 
    C_loiter = engines_sfc_table[engine][1]
    return C_cruise, C_loiter

#---------------------------------------------------------------------------------------------

## Errors :
#   for   - Flying boat
#         - Jet trainer
#         - Jet Fighter
#  W0 weight negative
#  We_W0 and Wf_W0  summation must be less than 1 (actually less than 0.9 or something if we consider w_payload)
# one solution to make weight positive is to add   "abs" to denominator in W0 = W_payload / abs(***)
# this solution is used but better one is required
##

