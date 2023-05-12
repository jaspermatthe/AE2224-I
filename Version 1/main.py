import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from data_pre_process import *
excel_path = Path(r'/home/jasper/Documents/data_group_c09/Data_C09_Integral.xls')

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

# sort based on alpha range -12 to
prop_V30 = sort_alpha_range(prop_28_32, alpha_index)
regen_V30 = sort_alpha_range(regen_28_32, alpha_index)

print(type(prop_V30))
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

# final sort
prop_beta15_neg12, prop_beta15_neg10, prop_beta15_neg8, prop_beta15_neg6, prop_beta15_neg4, prop_beta15_neg2, prop_beta15_0, prop_beta15_2, prop_beta15_4, prop_beta15_6, prop_beta15_8, prop_beta15_10, prop_beta15_12 = sort_alpha_value(
  prop_V30_beta15, alpha_index)

prop_beta30_neg12, prop_beta30_neg10, prop_beta30_neg8, prop_beta30_neg6, prop_beta30_neg4, prop_beta30_neg2, prop_beta30_0, prop_beta30_2, prop_beta30_4, prop_beta30_6, prop_beta30_8, prop_beta30_10, prop_beta30_12 = sort_alpha_value(
  prop_V30_beta30, alpha_index)

regen_beta15_neg12, regen_beta15_neg10, regen_beta15_neg8, regen_beta15_neg6, regen_beta15_neg4, regen_beta15_neg2, regen_beta15_0, regen_beta15_2, regen_beta15_4, regen_beta15_6, regen_beta15_8, regen_beta15_10, regen_beta15_12 = sort_alpha_value(
  regen_V30_beta15, alpha_index)

regen_beta30_neg12, regen_beta30_neg10, regen_beta30_neg8, regen_beta30_neg6, regen_beta30_neg4, regen_beta30_neg2, regen_beta30_0, regen_beta30_2, regen_beta30_4, regen_beta30_6, regen_beta30_8, regen_beta30_10, regen_beta30_12 = sort_alpha_value(
  regen_V30_beta30, alpha_index)
"""
1: DATA PROCESSING
"""

# Retrieve relvant column indices for processing
FX_i_index = column_headers.index('FX_I')
I_index = column_headers.index('I_M')
n_index = column_headers.index('RPS_M')
rho_index = column_headers.index('rho_atm')

# Constants
D = 0.6  # check this

"""
2: DATA GRAPHING
"""
"""
Prop
"""
# plot V30, beta 15, alpha 0 FX_i vs. J
plt.plot(prop_beta15_0[:, J_index], prop_beta15_0[:, FX_i_index], 'o')
plt.xlabel('J')
plt.ylabel('FX_i')
plt.title('Propulsive, V30, beta 15, alpha 0')
plt.show()


# # Generate some random data
# J_prop_beta15_neg12 = prop_beta15_neg12[:, J_index]
# J_prop_beta15_neg10 = prop_beta15_neg10[:, J_index]
# J_prop_beta15_neg8 = prop_beta15_neg8[:, J_index]
# J_prop_beta15_neg6 = prop_beta15_neg6[:, J_index]
# J_prop_beta15_neg4 = prop_beta15_neg4[:, J_index]
# J_prop_beta15_neg2 = prop_beta15_neg2[:, J_index]
# J_prop_beta15_0 = prop_beta15_0[:, J_index]
# J_prop_beta15_2 = prop_beta15_2[:, J_index]
# J_prop_beta15_4 = prop_beta15_4[:, J_index]
# J_prop_beta15_6 = prop_beta15_6[:, J_index]
# J_prop_beta15_8 = prop_beta15_8[:, J_index]
# J_prop_beta15_10 = prop_beta15_10[:, J_index]
# J_prop_beta15_12 = prop_beta15_12[:, J_index]

# # now thrust
# Thrust_prop_beta15_neg12 = prop_beta15_neg12[:, FX_i_index]
# Thrust_prop_beta15_neg10 = prop_beta15_neg10[:, FX_i_index]
# Thrust_prop_beta15_neg8 = prop_beta15_neg8[:, FX_i_index]
# Thrust_prop_beta15_neg6 = prop_beta15_neg6[:, FX_i_index]
# Thrust_prop_beta15_neg4 = prop_beta15_neg4[:, FX_i_index]
# Thrust_prop_beta15_neg2 = prop_beta15_neg2[:, FX_i_index]
# Thrust_prop_beta15_0 = prop_beta15_0[:, FX_i_index]
# Thrust_prop_beta15_2 = prop_beta15_2[:, FX_i_index]
# Thrust_prop_beta15_4 = prop_beta15_4[:, FX_i_index]
# Thrust_prop_beta15_6 = prop_beta15_6[:, FX_i_index]
# Thrust_prop_beta15_8 = prop_beta15_8[:, FX_i_index]
# Thrust_prop_beta15_10 = prop_beta15_10[:, FX_i_index]
# Thrust_prop_beta15_12 = prop_beta15_12[:, FX_i_index]

# # now current
# I_prop_beta15_neg12 = prop_beta15_neg12[:, I_index]
# I_prop_beta15_neg10 = prop_beta15_neg10[:, I_index]
# I_prop_beta15_neg8 = prop_beta15_neg8[:, I_index]
# I_prop_beta15_neg6 = prop_beta15_neg6[:, I_index]
# I_prop_beta15_neg4 = prop_beta15_neg4[:, I_index]
# I_prop_beta15_neg2 = prop_beta15_neg2[:, I_index]
# I_prop_beta15_0 = prop_beta15_0[:, I_index]
# I_prop_beta15_2 = prop_beta15_2[:, I_index]
# I_prop_beta15_4 = prop_beta15_4[:, I_index]
# I_prop_beta15_6 = prop_beta15_6[:, I_index]
# I_prop_beta15_8 = prop_beta15_8[:, I_index]
# I_prop_beta15_10 = prop_beta15_10[:, I_index]
# I_prop_beta15_12 = prop_beta15_12[:, I_index]

# # plot I vs Thurst for all the above, add different markers for each scatter plot
# plt.scatter(Thrust_prop_beta15_neg12, I_prop_beta15_neg12, color='red', label='prop_beta15_neg12', marker='o')
# plt.scatter(Thrust_prop_beta15_neg10, I_prop_beta15_neg10, color='orange', label='prop_beta15_neg10', marker='o')
# plt.scatter(Thrust_prop_beta15_neg8, I_prop_beta15_neg8, color='yellow', label='prop_beta15_neg8', marker='o')
# plt.scatter(Thrust_prop_beta15_neg6, I_prop_beta15_neg6, color='green', label='prop_beta15_neg6', marker='o')
# plt.scatter(Thrust_prop_beta15_neg4, I_prop_beta15_neg4, color='blue', label='prop_beta15_neg4', marker='o')
# plt.scatter(Thrust_prop_beta15_neg2, I_prop_beta15_neg2, color='purple', label='prop_beta15_neg2', marker='o')
# plt.scatter(Thrust_prop_beta15_0, I_prop_beta15_0, color='black', label='prop_beta15_0', marker='o')
# plt.scatter(Thrust_prop_beta15_2, I_prop_beta15_2, color='red', label='prop_beta15_2', marker='o')
# plt.scatter(Thrust_prop_beta15_4, I_prop_beta15_4, color='orange', label='prop_beta15_4', marker='o')
# plt.scatter(Thrust_prop_beta15_6, I_prop_beta15_6, color='yellow', label='prop_beta15_6', marker='o')
# plt.scatter(Thrust_prop_beta15_8, I_prop_beta15_8, color='green', label='prop_beta15_8', marker='o')
# plt.scatter(Thrust_prop_beta15_10, I_prop_beta15_10, color='blue', label='prop_beta15_10', marker='o')
# plt.scatter(Thrust_prop_beta15_12, I_prop_beta15_12, color='purple', label='prop_beta15_12', marker='o')

# same I vs. Thrust for regen propellers
"""
Regen propellers
"""
# Generate some random data
# J_regen_beta15_neg12 = regen_beta15_neg12[:, J_index]
# J_regen_beta15_neg10 = regen_beta15_neg10[:, J_index]
# J_regen_beta15_neg8 = regen_beta15_neg8[:, J_index]
# J_regen_beta15_neg6 = regen_beta15_neg6[:, J_index]
# J_regen_beta15_neg4 = regen_beta15_neg4[:, J_index]
# J_regen_beta15_neg2 = regen_beta15_neg2[:, J_index]
# J_regen_beta15_0 = regen_beta15_0[:, J_index]
# J_regen_beta15_2 = regen_beta15_2[:, J_index]
# J_regen_beta15_4 = regen_beta15_4[:, J_index]
# J_regen_beta15_6 = regen_beta15_6[:, J_index]
# J_regen_beta15_8 = regen_beta15_8[:, J_index]
# J_regen_beta15_10 = regen_beta15_10[:, J_index]
# J_regen_beta15_12 = regen_beta15_12[:, J_index]

# # now thrust
# Thrust_regen_beta15_neg12 = regen_beta15_neg12[:, FX_i_index]
# Thrust_regen_beta15_neg10 = regen_beta15_neg10[:, FX_i_index]
# Thrust_regen_beta15_neg8 = regen_beta15_neg8[:, FX_i_index]
# Thrust_regen_beta15_neg6 = regen_beta15_neg6[:, FX_i_index]
# Thrust_regen_beta15_neg4 = regen_beta15_neg4[:, FX_i_index]
# Thrust_regen_beta15_neg2 = regen_beta15_neg2[:, FX_i_index]
# Thrust_regen_beta15_0 = regen_beta15_0[:, FX_i_index]
# Thrust_regen_beta15_2 = regen_beta15_2[:, FX_i_index]
# Thrust_regen_beta15_4 = regen_beta15_4[:, FX_i_index]
# Thrust_regen_beta15_6 = regen_beta15_6[:, FX_i_index]
# Thrust_regen_beta15_8 = regen_beta15_8[:, FX_i_index]
# Thrust_regen_beta15_10 = regen_beta15_10[:, FX_i_index]
# Thrust_regen_beta15_12 = regen_beta15_12[:, FX_i_index]

# # now current
# I_regen_beta15_neg12 = regen_beta15_neg12[:, I_index]
# I_regen_beta15_neg10 = regen_beta15_neg10[:, I_index]
# I_regen_beta15_neg8 = regen_beta15_neg8[:, I_index]
# I_regen_beta15_neg6 = regen_beta15_neg6[:, I_index]
# I_regen_beta15_neg4 = regen_beta15_neg4[:, I_index]
# I_regen_beta15_neg2 = regen_beta15_neg2[:, I_index]
# I_regen_beta15_0 = regen_beta15_0[:, I_index]
# I_regen_beta15_2 = regen_beta15_2[:, I_index]
# I_regen_beta15_4 = regen_beta15_4[:, I_index]
# I_regen_beta15_6 = regen_beta15_6[:, I_index]
# I_regen_beta15_8 = regen_beta15_8[:, I_index]
# I_regen_beta15_10 = regen_beta15_10[:, I_index]
# I_regen_beta15_12 = regen_beta15_12[:, I_index]

# # plot I vs Thurst for all the above, add different markers for each scatter plot
# plt.scatter(Thrust_regen_beta15_neg12, I_regen_beta15_neg12, color='red', label='regen_beta15_neg12', marker='x')
# plt.scatter(Thrust_regen_beta15_neg10, I_regen_beta15_neg10, color='orange', label='regen_beta15_neg10', marker='x')
# plt.scatter(Thrust_regen_beta15_neg8, I_regen_beta15_neg8, color='yellow', label='regen_beta15_neg8', marker='x')
# plt.scatter(Thrust_regen_beta15_neg6, I_regen_beta15_neg6, color='green', label='regen_beta15_neg6', marker='x')
# plt.scatter(Thrust_regen_beta15_neg4, I_regen_beta15_neg4, color='blue', label='regen_beta15_neg4', marker='x')
# plt.scatter(Thrust_regen_beta15_neg2, I_regen_beta15_neg2, color='purple', label='regen_beta15_neg2', marker='x')
# plt.scatter(Thrust_regen_beta15_0, I_regen_beta15_0, color='black', label='regen_beta15_0', marker='o')
# plt.scatter(Thrust_regen_beta15_2, I_regen_beta15_2, color='red', label='regen_beta15_2', marker='o')
# plt.scatter(Thrust_regen_beta15_4, I_regen_beta15_4, color='orange', label='regen_beta15_4', marker='o')
# plt.scatter(Thrust_regen_beta15_6, I_regen_beta15_6, color='yellow', label='regen_beta15_6', marker='o')
# plt.scatter(Thrust_regen_beta15_8, I_regen_beta15_8, color='green', label='regen_beta15_8', marker='o')
# plt.scatter(Thrust_regen_beta15_10, I_regen_beta15_10, color='blue', label='regen_beta15_10', marker='o')
# plt.scatter(Thrust_regen_beta15_12, I_regen_beta15_12, color='purple', label='regen_beta15_12', marker='o')

# plt.xlabel('Thrust (N)')
# plt.ylabel('Current (A)')
# plt.title('Thrust vs Current for Regen Braking, Beta = 15')
# plt.legend(loc='upper left')
# plt.grid()
# plt.show()


