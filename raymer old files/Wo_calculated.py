a=1.34
c=-0.13
Wp=11212.708
Wf_f=0.56295954

Wo_guess = float(input("Wo_guess = "))
We_f = a*(Wo_guess**c)
Wo_calc = (Wp)/(1-We_f-Wf_f)


while Wo_guess != Wo_calc :
    Wo_guess = Wo_calc
    We_f = a*(Wo_guess**c)
    Wo_calc = (Wp)/(1-We_f-Wf_f)

print("Wo_calculated = ", Wo_calc)
