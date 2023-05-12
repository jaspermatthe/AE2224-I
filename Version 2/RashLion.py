import matplotlib.pyplot as plt
import numpy as np

#Define input arrays


#calculate the rotational speed
def rot_speed(RPS, n):
  n = RPS / n
  return n


#Define the thrust coefficent
def thrust_coeff(T, rho, n, D):
  C_T = -T / (rho * n**2 * D**4)
  return C_T


#DEFINE the power coefficient
def power_coeff(Q, rho, n, D):
  C_P = Q / (rho * n**2 * D**5)
  return C_P


#Calculate the thrust and power coeffcients
C_T = thrust_coeff(T, rho, n, D)
C_P = power_coeff(Q, rho, n, D)

#plot Ct and Cp against J
fig, ax = plt.subplots()
ax.plot(J, C_T, label="Thrust Coefficient")
ax.plot(J, C_P, label="Power Coefficient")
ax.set_xlabel("Advance Ratio (J)")
ax.set_title("Thrust and Power Coefficients vs Advance Ratio")
ax.legend()

#plot C_T against C_P
fig, ax = plt.subplots()
ax.plot(C_P, C_T)
ax.set_xlabel("Power Coefficient (C_P)")
ax.set_ylabel("Thrust Coefficient (C_T)")
plt.show()


