import numpy as np
def decompose_forces_local_to_global(alpha, FX_local, FY_local, FZ_local):
    """
    parameters:
    alpha (np.array): angle of attack of propeller 
    FX_local (np.array): force in local x coordinate frame direction from internal or external force balance
    FY_local (np.array): force in local y coordinate frame direction from internal or external force balance
    FZ_local (np.array): force in local z coordinate frame direction from internal or external force balance

    returns:
    FX_global (np.array): force in global x coordinate frame by decomposition with alpha
    FY_global (np.array): force in global y coordinate frame by decomposition with alpha
    FZ_global (np.array): force in global z coordinate frame by decomposition with alpha
    """
    alpha_rad = np.deg2rad(alpha)
    cos_alpha = np.cos(alpha_rad)
    
    FX_global = FX_local * cos_alpha 
    FZ_global = FZ_local * cos_alpha
    FY_global = FY_local # y-direction is not affected by changes in AoA
    
    return FX_global, FY_global, FZ_global

# J = np_array[:, 13]
# #define some of the functions, necessary for eff
# I = np_array[:, 15]
# V = np_array[:, 14]
# rps = np_array[:, 11]

def efficiency():
  P_electric = I * V
  P_motor = rps * Mx
  electric_eff = P_motor/P_electric
  regen_eff = P_electric/P_motor
  propulsive_eff = (C_T*J)/(2*np.pi*C_P)
  return propulsive_eff and regen_eff and electric_eff

# def graph():
#   for every beta in range(15, 30, 15):
# 	  for every J in range(0.55, 1.50):
# 		  for every alpha in range(-12, 12):

			# decompose internal balance forces and moments into global coordinate system
			# decompose external balance forces and moments into global coordinate system
			# compute C_T and C_Q coefficients for internal
			# compute C_T and C_Q coefficients for external