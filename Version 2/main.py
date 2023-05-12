from data_preprocessing import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# from calculations import *
# from Jasper_M import decompose_forces_local_to_global
import numpy as np

# sort by Vinf. done
# sort by beta. done
# sort by regen/prop. done 
# sort by J for each
# calculate Cp
# calculate Ct
# plot Cp vs. alpha


"""
Pre-Processing:

Splitting data into:
- regenerative and propulsive regimes by I_M (current) values
- blade angles: 15 and 30 deg
- AoA: steps of 2 between and including -12 and 12 deg
- J: between 0.55-1.50 for beta 15 deg
- J: between 0.90-2.10 for beta 30 deg

Final number of arrays is 52:
- 13 propulsive beta = 15 deg: alpha -12 to 12 deg, 0.55<=J<=1.50
- 13 propulsive beta = 30 deg: alpha -12 to 12 deg, 0.55<=J<=1.50
- 13 regen beta = 15 deg: alpha -12 to 12 deg, 0.90<=J<=2.10
- 13 regen beta = 30 deg: alpha -12 to 12 deg, 0.90<=J<=2.10
"""

# Retrieve Indices of Relevant Columns for Pre-Processing
column_headers = [
    'DPN', 'time', 'p_Atm', 'T_atm', 'rho_atm', 'mu_atm', 'gamma_atm', 'Qinf',
    'Vinf', 'AoA', 'beta', 'RPS_M', 'StdDevRPS', 'J', 'V_M', 'I_M', 'T_M',
    'PSus', 'PTus', 'FX_I', 'FY_I', 'FZ_I', 'MX_I', 'MY_I', 'MZ_I', 'FX_E',
    'FY_E', 'FZ_E', 'MX_E', 'MY_E', 'MZ_E'
]

V_index = column_headers.index('Vinf')
alpha_index = column_headers.index('AoA')
beta_index = column_headers.index('beta')
J_index = column_headers.index('J')

# split into propulsive and regenerative regimes based on value of current, 'I_M'
data_propulsive, data_regen = filter_prop_regen(excel_path)

# split propulsive and regenerative regimes into 20, 30, 40, and other m/s
prop_18_22, prop_28_32, prop_38_42, prop_other = sort_Vinf(
    data_propulsive, V_index)
regen_18_22, regen_28_32, regen_38_42, regen_other = sort_Vinf(
    data_regen, V_index)

# sort based on alpha range -12 to 12
prop_V30 = sort_alpha_range(prop_28_32, alpha_index)
regen_V30 = sort_alpha_range(regen_28_32, alpha_index)

# sort based on beta
prop_V30_beta15, prop_V30_beta30 = sort_beta(prop_V30, beta_index)
regen_V30_beta15, regen_V30_beta30 = sort_beta(regen_V30, beta_index)

# sort based on J as specified per beta in reader
prop_V30_beta15 = sort_J(prop_V30_beta15, J_index, 0.55, 1.50)
prop_V30_beta30 = sort_J(prop_V30_beta30, J_index, 0.90, 2.10)
regen_V30_beta15 = sort_J(regen_V30_beta15, J_index, 0.55, 1.50)
regen_V30_beta30 = sort_J(regen_V30_beta30, J_index, 0.90, 2.10)

# problem because we don't get the full range of J for each regime
print(min(prop_V30_beta15[:, J_index]), '<= J prop V30 beta 15 <=',
      max(prop_V30_beta15[:, J_index]))
print(min(prop_V30_beta30[:, J_index]), '<= J prop V30 beta 30 <=',
      max(prop_V30_beta30[:, J_index]))
print(min(regen_V30_beta15[:, J_index]), '<= J regen V30 beta 15 <=',
      max(regen_V30_beta15[:, J_index]))
print(min(regen_V30_beta30[:, J_index]), '<= J regen V30 beta 30 <=',
      max(regen_V30_beta30[:, J_index]))

# for each operational condition where V, beta, and prop/regen are constant, sort into bins of J

"""
1: DATA PROCESSING
"""

# Retrieve relevant column indices for processing
FX_i_index = column_headers.index('FX_I')
I_index = column_headers.index('I_M')
n_index = column_headers.index('RPS_M')
rho_index = column_headers.index('rho_atm')
Q_index = column_headers.index('MZ_E')
FY_i_index = column_headers.index('FY_I')
FZ_i_index = column_headers.index('FZ_I')
FZ_e_index = column_headers.index('FZ_E')

# Constants
D = 0.6  # check this


# # Initialize an empty list to hold the sliced arrays
# sliced_arrays_J = []
# sliced_arrays_T = []
# sliced_arrays_Q = []
# sliced_arrays_rho = []
# sliced_arrays_n = []
# sliced_arrays_RPS = []
# sliced_arrays_FX = []
# sliced_arrays_FY = []
# sliced_arrays_FZ = []
# sliced_arrays_alpha = []


# # Loop over the input arrays and slice them
# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, J_index]
#     sliced_arrays_J.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, n_index]
#     sliced_arrays_n.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, rho_index]
#     sliced_arrays_rho.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, n_index]
#     sliced_arrays_RPS.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, FX_i_index]
#     sliced_arrays_FX.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, FY_i_index]
#     sliced_arrays_FY.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, FZ_i_index]
#     sliced_arrays_FZ.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, alpha_index]
#     sliced_arrays_alpha.append(sliced_arr)

# for arr in [prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12, prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12, regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12, regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#     sliced_arr = arr[:, Q_index]
#     sliced_arrays_Q.append(sliced_arr)

# # Stack the sliced arrays into a new array
# result_array_J = np.column_stack(sliced_arrays_J)
# result_array_n = np.full_like(result_array_J, 3)
# result_array_rho = np.column_stack(sliced_arrays_rho)
# result_array_RPS = np.column_stack(sliced_arrays_RPS)
# result_array_D = np.full_like(result_array_J, 0.6)
# result_array_FX = np.column_stack(sliced_arrays_FX)
# result_array_FY = np.column_stack(sliced_arrays_FY)
# result_array_FZ = np.column_stack(sliced_arrays_FZ)
# result_array_alpha = np.column_stack(sliced_arrays_alpha)
# result_array_Q =np.column_stack(sliced_arrays_Q)
# result_array_T, y, z, = decompose_forces_local_to_global(result_array_alpha, result_array_FX, result_array_FY, result_array_FZ)

# print (result_array_T)

#Define the thrust coefficent
def thrust_coeff(T, rho, n, D):
    C_T = T / (rho * n**2 * D**4)
    return C_T
print("raash")

#DEFINE the power coefficient
def power_coeff(Q, rho, n, D):
    C_P = Q *2*np.pi / (rho* n**2 * D**5)
    return C_P



# def efficiency(data,I_M, V_M, RPS_M, MZ_E):
#     P_electric = data[:,I_index] * data[:,V_index]
#     P_motor = rps * Mx
#     electric_eff = P_motor/P_electric
#     regen_eff = P_electric/P_motor
#     propulsive_eff = (C_T*J)/(2*np.pi*C_P)
#     return propulsive_eff and regen_eff and electric_eff

# def Reynolds(Vinf, rho_atm, mu_atm):
#     chord = 31.10905 * 10**-3
#     Reynolds_number = Vinf * chord * rho_atm / mu_atm
#     return Reynolds_number
#     plt.text(x=0.58, y=-0.05, s=r'$\beta = 15\degree$\nSome additional text', fontsize=16, verticalalignment='bottom', fontdict=None)

# print(np.average(Reynolds()))

print("gjshgh")
# C_T_lst = []
# C_P_lst =[]
# # #Finding the C_T and C_P
# for i in range(len(result_array_J)):
#   C_T = thrust_coeff(T = result_array_T[i], rho = result_array_rho[i], n = result_array_n[i], D= result_array_D[i])
#   C_P = power_coeff(Q =result_array_Q[i], rho =result_array_rho[i], n =result_array_n[i], D =result_array_D[i])
#   C_T_lst.append(C_T)
#   C_P_lst.append(C_P)


# J = np_array[:, 13]
# #define some of the functions, necessary for eff
# I = np_array[:, 15]
# V = np_array[:, 14]
# rps = np_array[:, 11]
# # Calculate the thrust and power coefficients
# C_T = thrust_coeff(T, rho, n, D)
# C_P = power_coeff(Q, rho, n, D)

# #propulsive_eff, regen_eff, electric_eff = efficiency(I = sliced_arrays_I, V=sliced_arrays_V, n = sliced_arrays_n, MX = sliced_arrays_MX, J = sliced_arrays_J, C_T, C_P)
# """
# 2: DATA GRAPHING
# """
# "Propulsive regime"
# fig, axs =plt.subplots(nrows =4 , ncols = 4, figsize =(16,12))
# #Plotting it (beta = 15, Ct vs. J)
# axs[0,0].

# T = decompose_forces_local_to_global(prop_beta15_neg12[:, alpha_index], prop_beta15_neg12[:, FX_i_index], prop_beta15_neg12[:, FY_i_index], prop_beta15_neg12[:, FZ_i_index])[0]

# C_T = thrust_coeff(T, rho = prop_beta15_neg12[:, rho_index], n = prop_beta15_neg12[:, n_index], D= 0.6)

# plt.scatter(prop_beta15_neg12[:, J_index], C_T)
# plt.show()

#prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10
# for prop_beta15_aoa in [prop_beta15_0, prop_beta15_neg12, prop_beta15_12]:
#    #T= decompose_forces_local_to_global(prop_beta15_aoa[:, alpha_index], prop_beta15_aoa[:, FX_i_index], prop_beta15_aoa[:, FY_i_index], prop_beta15_aoa[:, FZ_i_index])[2]
#    T = -1*prop_beta15_aoa[:,FZ_e_index]
#    C_T =thrust_coeff(T, rho = prop_beta15_aoa[:, rho_index], n = prop_beta15_aoa[:, n_index], D= 0.4064)
#    plt.scatter(prop_beta15_aoa[:, J_index], C_T)

# plt.ylabel("Thrust")
# plt.xlabel("Advance ratio")
# plt.show()

""""for prop_beta30_aoa in [prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12]:
  #T= decompose_forces_local_to_global(prop_beta30_aoa[:, alpha_index], prop_beta30_aoa[:, FX_i_index], prop_beta30_aoa[:, FY_i_index], prop_beta30_aoa[:, FZ_i_index])[2]  
  C_T =thrust_coeff(T, rho = prop_beta30_aoa[:, rho_index], n = prop_beta30_aoa[:, n_index], D= 0.6)
  plt.scatter(prop_beta30_aoa[:, J_index], C_T)

plt.ylabel("Thrust")
plt.xlabel("Advance ratio")
plt.show()"""

""""for regen_beta15_aoa in [regen_beta15_neg12, regen_beta15_0,regen_beta15_12]:
   #T= decompose_forces_local_to_global(regen_beta15_aoa[:, alpha_index], regen_beta15_aoa[:, FX_i_index], regen_beta15_aoa[:, FY_i_index], regen_beta15_aoa[:, FZ_i_index])[2]
   T =-1*regen_beta15_aoa[:, FZ_e_index]
   C_T =thrust_coeff(T, rho = regen_beta15_aoa[:, rho_index], n = regen_beta15_aoa[:, n_index], D= 0.4064)
   plt.scatter(regen_beta15_aoa[:, J_index], C_T) 

plt.ylabel("Thrust")
plt.xlabel("Advance ratio")
plt.show() """

# for regen_beta15_aoa in [regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12]:
#    T = -1*regen_beta15_aoa[:, FZ_e_index]
#    C_T = thrust_coeff(T, rho=regen_beta15_aoa[:, rho_index], n=regen_beta15_aoa[:, n_index], D=0.4064)
#    plt.scatter(regen_beta15_aoa[:, J_index], C_T, label=f"Angle of Attack: {regen_beta15_aoa[0, alpha_index]:.0f} degrees", s=10)

# plt.ylabel("Thrust")
# plt.xlabel("Advance ratio")
# plt.legend()
# plt.show()

# for regen_beta30_aoa in [regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#   T= decompose_forces_local_to_global(regen_beta30_aoa[:, alpha_index], regen_beta30_aoa[:, FX_i_index], regen_beta30_aoa[:, FY_i_index], regen_beta30_aoa[:, FZ_i_index])[2]
#   C_T =thrust_coeff(T, rho = regen_beta30_aoa[:, rho_index], n = regen_beta30_aoa[:, n_index], D= 0.6)
#   plt.scatter(regen_beta30_aoa[:, J_index], C_T)

# plt.ylabel("Thrust")
# plt.xlabel("Advance ratio")
# plt.show()



# for i in range(24):
#     # Modify the data here according to your needs
#     data_x = prop_beta15_neg12[:, i]
#     data_y = C_T

#     # Create a new plot for each iteration
#     plt.scatter(data_x, data_y)

#     # Save or show the plot, depending on your preference
#     plt.savefig(f"plot_{i}.png") # Saves each plot as a PNG file with a unique filename
#     plt.show() # Shows each plot on the screen


# import os

# # Create the directory if it doesn't already exist
# if not os.path.exists("plots"):
#     os.mkdir("plots")

# # Plot some data
# for regen_beta15_aoa in [regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12]:
#    T = -1*regen_beta15_aoa[:, FZ_e_index]
#    C_T = thrust_coeff(T, rho=regen_beta15_aoa[:, rho_index], n=regen_beta15_aoa[:, n_index], D=0.4064)
#    plt.scatter(regen_beta15_aoa[:, J_index], C_T, label=f"Angle of Attack: {regen_beta15_aoa[0, alpha_index]:.0f} degrees", s=10)

# plt.ylabel("Thrust")
# plt.xlabel("Advance ratio")
# plt.legend()
# plt.show()

# for regen_beta30_aoa in [regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12]:
#   T= decompose_forces_local_to_global(regen_beta30_aoa[:, alpha_index], regen_beta30_aoa[:, FX_i_index], regen_beta30_aoa[:, FY_i_index], regen_beta30_aoa[:, FZ_i_index])[2]
#   C_T =thrust_coeff(T, rho = regen_beta30_aoa[:, rho_index], n = regen_beta30_aoa[:, n_index], D= 0.6)
#   plt.scatter(regen_beta30_aoa[:, J_index], C_T)

# plt.ylabel("Thrust")
# plt.xlabel("Advance ratio")
# plt.show()


# # Save the plot to a file
# plt.savefig("plots/my_plot.png")


#Plotting the graphs
#NOTE: no more decomposing forces, we use FZ_E for thrust, we do -1
import os

# Create the plots folder if it doesn't exist
if not os.path.exists("Plots"):
    os.mkdir("Plots")

#firstly, for the beta 15, prop, ct-j
markers = ['x', '.', '1', '+', 1, '_', '2']
for i, prop_beta15_aoa in enumerate([prop_beta15_neg12, prop_beta15_neg8, prop_beta15_neg4, prop_beta15_0, prop_beta15_4, prop_beta15_8, prop_beta15_12]):
    T = -1*prop_beta15_aoa[:, FZ_e_index]
    C_T = thrust_coeff(T, rho=prop_beta15_aoa[:, rho_index], n=prop_beta15_aoa[:, n_index], D=0.4064)
    plt.scatter(prop_beta15_aoa[:, J_index], C_T, color='k', label=f"Angle of Attack: {prop_beta15_aoa[0, alpha_index]:.0f} degrees", s=50, marker = markers[i])

plt.text(x=0.58, y=-0.02, s='Propulsive Setting'+'\n'r'          $\beta = 15\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Thrust Coefficient " + u'C\u1D1B')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta15_prop_ct-j.png")
plt.show()

#secondly, for the beta 30, prop, ct-j
for prop_beta30_aoa in [prop_beta30_neg12, prop_beta30_neg8, prop_beta30_neg4, prop_beta30_0, prop_beta30_4, prop_beta30_8, prop_beta30_12]:
   T = -1*prop_beta30_aoa[:, FZ_e_index]
   C_T = thrust_coeff(T, rho=prop_beta30_aoa[:, rho_index], n=prop_beta30_aoa[:, n_index], D=0.4064)
   plt.scatter(prop_beta30_aoa[:, J_index], C_T, label=f"Angle of Attack: {prop_beta30_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=1.0, y=0.010, s='Propulsive Setting'+'\n'r'          $\beta = 30\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Thrust Coefficient " + u'C\u1D1B')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta30_prop_ct-j.png")
plt.show()

# #thirdly, for the beta 15, reg, ct-j
for reg_beta15_aoa in [regen_beta15_neg12, regen_beta15_neg8, regen_beta15_neg4, regen_beta15_0, regen_beta15_4, regen_beta15_8, regen_beta15_12]:
   T = -1*reg_beta15_aoa[:, FZ_e_index]
   C_T = thrust_coeff(T, rho=reg_beta15_aoa[:, rho_index], n=reg_beta15_aoa[:, n_index], D=0.4064)
   plt.scatter(reg_beta15_aoa[:, J_index], C_T, label=f"Angle of Attack: {reg_beta15_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=0.9, y=-0.175, s='Regenerative Setting'+'\n'r'          $\beta = 15\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Thrust Coefficient " + u'C\u1D1B')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta15_reg_ct-j.png")
plt.show()

# #fourthly, for the beta 30, reg, ct-j
for reg_beta30_aoa in [regen_beta30_neg12, regen_beta30_neg8, regen_beta30_neg4, regen_beta30_0, regen_beta30_4, regen_beta30_8, regen_beta30_12]:
   T = -1*reg_beta30_aoa[:, FZ_e_index]
   C_T = thrust_coeff(T, rho=reg_beta30_aoa[:, rho_index], n=reg_beta30_aoa[:, n_index], D=0.4064)
   plt.scatter(reg_beta30_aoa[:, J_index], C_T, label=f"Angle of Attack: {reg_beta30_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=1.85, y=-0.04, s='Regenerative Setting'+'\n'r'          $\beta = 30\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Thrust Coefficient " + u'C\u1D1B')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta30_reg_ct-j.png")
plt.show()

#fifthly, for the beta 15, prop, cp-j
for prop_beta15_aoa in [prop_beta15_neg12, prop_beta15_neg8, prop_beta15_neg4, prop_beta15_0, prop_beta15_4, prop_beta15_8, prop_beta15_12]:
    #  T = -1*prop_beta15_aoa[:, FZ_e_index]
    #  C_P = thrust_coeff(T, rho=reg_beta30_aoa[:, rho_index], n=reg_beta30_aoa[:, n_index], D=0.4064)
    Q = prop_beta15_aoa[:, Q_index]
    C_P = power_coeff(Q, rho=prop_beta15_aoa[:, rho_index], n=prop_beta15_aoa[:, n_index], D=0.4064)
    plt.scatter(prop_beta15_aoa[:, J_index], C_P, label=f"Angle of Attack: {prop_beta15_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=0.715, y=0.045, s='Propulsive Setting'+'\n'r'          $\beta = 15\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Power Coefficient  "+ u'C\u1D18')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta15_prop_cp-j.png")
plt.show()

# #sixthly, for the beta 30, prop, cp-j
for prop_beta30_aoa in [prop_beta30_neg12, prop_beta30_neg8, prop_beta30_neg4, prop_beta30_0, prop_beta30_4, prop_beta30_8, prop_beta30_12]:
  #  T = -1*prop_beta15_aoa[:, FZ_e_index]
  #  C_P = thrust_coeff(T, rho=reg_beta30_aoa[:, rho_index], n=reg_beta30_aoa[:, n_index], D=0.4064)
  Q = prop_beta30_aoa[:, Q_index]
  C_P = power_coeff(Q, rho=prop_beta30_aoa[:, rho_index], n=prop_beta30_aoa[:, n_index], D=0.4064)
  plt.scatter(prop_beta30_aoa[:, J_index], C_P, label=f"Angle of Attack: {prop_beta30_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=1.3, y=0.14, s='Propulsive Setting'+'\n'r'          $\beta = 30\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Power Coefficient  "+ u'C\u1D18')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta30_prop_cp-j.png")
plt.show()

# #seventhly, for the beta 15, reg, cp-j
for reg_beta15_aoa in [regen_beta15_neg12, regen_beta15_neg8, regen_beta15_neg4, regen_beta15_0, regen_beta15_4, regen_beta15_8, regen_beta15_12]:
  Q = reg_beta15_aoa[:, Q_index]
  C_P = power_coeff(Q, rho=reg_beta15_aoa[:, rho_index], n=reg_beta15_aoa[:, n_index], D=0.4064)
  plt.scatter(reg_beta15_aoa[:, J_index], C_P, label=f"Angle of Attack: {reg_beta15_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=0.95, y=-0.12, s='Regenerative Setting'+'\n'r'          $\beta = 15\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Power Coefficient  "+ u'C\u1D18')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta15_reg_cp-j.png")
plt.show()

# #eightly, for the beta 30, reg, cp-j
for reg_beta30_aoa in [regen_beta30_neg12, regen_beta30_neg8, regen_beta30_neg4, regen_beta30_0, regen_beta30_4, regen_beta30_8, regen_beta30_12]:
  Q = reg_beta30_aoa[:, Q_index]
  C_P = power_coeff(Q, rho=reg_beta30_aoa[:, rho_index], n=reg_beta30_aoa[:, n_index], D=0.4064)
  plt.scatter(reg_beta30_aoa[:, J_index], C_P, label=f"Angle of Attack: {reg_beta30_aoa[0, alpha_index]:.0f} degrees", s=10)

plt.text(x=1.85, y=0.03, s='Regenerative Setting'+'\n'r'          $\beta = 30\degree$', fontsize=10, weight = 'bold')
plt.ylabel("Power Coefficient  "+ u'C\u1D18')
plt.xlabel("Advance ratio")
plt.legend(fontsize="small")
plt.savefig("Plots/beta30_reg_cp-j.png")
plt.show()

#ninethly, for the beta 15, prop, efficiency-j

#tenthly, for the beta 30, prop, efficiency-j
#eleventhly, for the beta 15, reg, efficiency-j
#twenthly, for the beta 30, reg, efficiency-j
#thirteenthly, for the beta 15, prop, ct-cp
#fourteenthly, for the beta 30, prop, ct-cp
#fifteenthly, for the beta 15, reg, ct-cp
#sixteenthly, for the beta 30, reg, ct-cp