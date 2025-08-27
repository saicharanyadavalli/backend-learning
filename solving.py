#import math
#arr = [0.01,0.02,0.03,0.04,0.05,0.1,0.3,0.5,0.7,0.9,1]
#arr2 = []
#for i in range(len(arr)):
#    arr2.append(round(5.31/arr[i],2))
#arr3 = []
#for i in range(len(arr2)):
#    arr3.append(round(239.6/math.sqrt(arr2[i]**2 + 5.855**2),2))
#arr4 = []
#for i in range(len(arr2)):
#    arr4.append(round(-1*(math.degrees(math.atan(5.855 / arr2[i]))),2))
#arr5 = []
#for i in range(len(arr2)):
#    arr5.append(round((3 * arr3[i] * arr3[i] * 5.31) / arr[i], 2))
#arr6 = []
#for i in range(len(arr2)):
#    arr6.append(round((3 * arr3[i] * arr3[i] * 5.31), 2))
#pout = []
#for i in range(len(arr3)):
#    pout.append(arr5[i]-arr6[i])
#arr8 = []
#for i in range(len(arr)):
#    arr8.append(round(1500*(1-arr[i])))
#arr9 = []
#for i in range(len(arr)):
#    try:
#        arr9.append(round((pout[i]*60)/(2*math.pi*arr8[i]),2))
#    except:
#        arr9.append(0)
#import cmath
#
#arr10 = []
#
#def polar_to_rect(magnitude, angle_deg):
#    angle_rad = math.radians(angle_deg)
#    return magnitude * (math.cos(angle_rad) + 1j * math.sin(angle_rad))
#
#def rect_to_polar(z):
#    magnitude = abs(z)
#    angle_deg = math.degrees(cmath.phase(z))
#    return magnitude, angle_deg
#
#magnitudes = []
#angles = []
#
#I1 = polar_to_rect(3.5, -72.42)
#for i in range(len(arr3)):
#    I2 = polar_to_rect(arr3[i],arr4[i])
#    I = I1 + I2
#    mag, ang = rect_to_polar(I)
#    arr10.append(f" {mag:.2f} ∠ {ang:.2f}° ")
#    magnitudes.append(round(mag, 2))
#    angles.append(round(ang, 2))
#
#pin = []
#for i in range(len(arr)):
#    angle_rad = math.radians(angles[i])
#    value = 3 * 239.6 * magnitudes[i] * math.cos(angle_rad)
#    pin.append(round(value, 2))
#
#effeciency = []
#for i in range(len(arr)):
#    effeciency.append(round((pout[i]/pin[i])*100,2))
#
#pf = []
#for i in range(len(arr)):
#    angle_rad = math.radians(angles[i])
#    value = math.cos(angle_rad)
#    pf.append(round(value,3))
#torque = [2.05, 4.11, 6.16, 8.21, 10.27, 20.45, 55.82, 79.2, 90.55, 93.66, 0]
#for i in range(len(torque)):
#    print(torque[i]/5)

values = [19,53,107,160,216,280,320,360,380,400,420,432,445,457,465]
vphase = []
for i in range(len(values)):
    vphase.append(round(values[i]/1.732,1))
isc = [0.3,0.8,1.43,2.04,2.62,3.49,4.1,4.6,5.32,6.04,6.7,6.9]
imp = []
for i in range(min(len(isc),len(values))):
    imp.append(round(vphase[i]/isc[i],2))

import math

# Given data
V = 415          # Terminal voltage (V)
Ia = 6.9        # Armature current (A)
Re = 3.9         # Effective resistance (ohm)
Xs = 38.25       # Synchronous reactance (ohm)

# List of power factor cosφ values
cos_phi_values = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

print(f"{'cosφ':<6}{'E0_lag (V)':<15}{'Reg_lag (%)':<15}{'E0_lead (V)':<15}{'Reg_lead (%)':<15}")
print("-"*70)

for cos_phi in cos_phi_values:
    sin_phi = math.sqrt(1 - cos_phi**2)  # since sin²φ + cos²φ = 1

    # Lagging PF (+ jXs term)
    E0_lag = math.sqrt((V*cos_phi + Ia*Re)**2 + (V*sin_phi + Ia*Xs)**2)
    reg_lag = ((E0_lag - V) / V) * 100

    # Leading PF (- jXs term)
    E0_lead = math.sqrt((V*cos_phi + Ia*Re)**2 + (V*sin_phi - Ia*Xs)**2)
    reg_lead = ((E0_lead - V) / V) * 100

    print(f"{cos_phi:<6}{E0_lag:<15.2f}{reg_lag:<15.2f}{E0_lead:<15.2f}{reg_lead:<15.2f}")

