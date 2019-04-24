# Aircaft Conceptual Design, Raymer
# ch: 03
# Weight Estimation

# Author : Parth Viradiya
# Update History:
#       - created file, 24-Apr-2019

# search ==>> @@@

from math import exp, sqrt
from standard_atmosphere import standard_atmosphere

# @@@ right now everyting is hard coded, will updated for inputs in future

## Given Data
# Type of Aircraft: Jet Transport
num_passengers = 294
num_pilot = 3
num_crew = 6
total_people = num_passengers + num_crew + num_pilot
# W_payload inlcudes total_people weight (per passenger allowed weight = 143.5 kg)
W_payload = total_people*143.5*2.204 # lbs,   2.204 = conversion factor from kg to lbs
 
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
E = 15 * 60  # Loiter Endurance , 15 min , converted to seconds

## Take-off weight builtup
# Designed takeoff gross weight --> total aircraft weight at the begining of the mission
# aslo called Max takeoff weight, W0
# W0 = W_crew + W_payload + W_fuel + W_empty
# W_crew and W_payload are known since they are the design requirement
# unkowns are W_fuel and W_empty, - However they are both dependent on the total weight
# fractions
# We_W0 = W_empty/W0  # w_empty as a fraction of the total takeoff weight
# Wf_W0 = W_fuel/W0  # w_fuel as a fraction of the total takeoff weight

# W0 = (W_crew + W_payload) / (1 - We_W0 - Wf_W0)
# if we can estimate We_W0 and Wf_W0, we can determine W0


# Mission Profile 
# Mission segment weight estimation  @@@ give a range of pre-defined mission profile to choose from
# @@@ build automatic Mission segment weight fration using W(i) / W(i-1) # use of dictionary may be
# W1_W0  # warmup and takeoff
W1_W0 = 0.970    # from the historic data Table[3.2]
# W2_W1  # climb up
W2_W1 = 0.985    # from the historic data Table[3.2]
# W3_W2  # cruise to the destination, length of cruise == R1
W3_W2 = exp((-R1*c) / (V*L_by_D_cruise*3600))
# W4_W3  # descent
W4_W3 = 0.995
# W5_W4  # loiter about 15 min   # @@@ loiter time
W5_W4 = exp((-E*c) / (L_by_D_max*3600))
# W6_W5  # again climb to cruise
W6_W5 = 0.985    # from the historic data Table[3.2]
# W7_W6  # cruise, length of cruise == R2
W7_W6 = exp((-R2*c) / (V*L_by_D_cruise*3600))
# W8_W7  # descent
W8_W7 = 0.995
# W9_W8  # loiter about 15 min   # @@@ loiter time
W9_W8 = exp((-E*c) / (L_by_D_max*3600))
# W10_W9  # descent
W10_W9 = 0.995
# W11_W10  # landing and taxing 
W11_W10 = 0.995    # from the historic data Table[3.2] 

# W11 / W0    => Calculating Fuel Usage duing each segment of flight mission
W11_W0 = W1_W0 * W2_W1 * W3_W2 * W4_W3 * W5_W4 * W6_W5 * W7_W6 * W8_W7 * W9_W8 * W10_W9 * W11_W10


# Fuel weight estimation
# based on the mission profile
Wf_W0 = 1.06*(1 - W11_W0)


# Empty weight estimation
A = 1.02
C = -0.06
# We_W0 = A * W0**C   # curve-fitting equation
# have to guess W0
A=1.02
C=-0.06

W0_guess = 5000    # random guess
We_W0 = A*(W0_guess**C)
W0 = (W_payload) / (1 - We_W0 - Wf_W0)
while W0_guess != W0 :
    W0_guess = W0
    We_W0 = A*(W0_guess**C)
    W0 = (W_payload)/(1 - We_W0 - Wf_W0)
# returns W0

W_fuel = Wf_W0 * W0  # Fuel weight calcualtion
We_W0 = A * (W0**C)
W_empty = We_W0 * W0 # Empty weight calcualtio

# A and C are coefficients, can be determned from Table [3.1] ## @@@  make a table
del A   # delting A and C from the memory so that can assign those name ot different coefficients
del C

print('******************************************')
print('Wight Estimation')
print('--------------------')
print(f'Total weight: {W0:.3f} lbs')
print(f'Payload Weight: {W_payload:.3f} lbs')
print(f'Fuel Weight: {W_fuel:.3f} lbs')
print(f'Empty weight: {W_empty:.3f} lbs')
print('******************************************')
