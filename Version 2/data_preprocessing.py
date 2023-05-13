import pandas as pd
import numpy as np
from pathlib import Path

excel_path = Path(r'/home/jasper/Documents/data_group_c09/Version 2/Data_C09_Integral.xlsx')



def filter_prop_regen(filename):
  # Read the Excel file into a pandas DataFrame
  df = pd.read_excel(filename)

  # Get the index of the specified column header
  col_index = df.columns.get_loc('I_M')

  # Convert the DataFrame to a numpy array
  data = df.to_numpy()

  # Filter the rows based on the value in the specified column
  propulsive_mask = (data[:, col_index] > 0)
  data_propulsive = data[propulsive_mask]
  data_regen = data[~propulsive_mask]

  # Return the filtered data
  return data_propulsive, data_regen


def sort_Vinf(data_array, column_index):
  # Create empty arrays for each range
  arr_18_22 = np.empty((0, data_array.shape[1]))
  arr_28_32 = np.empty((0, data_array.shape[1]))
  arr_38_42 = np.empty((0, data_array.shape[1]))
  arr_other = np.empty((0, data_array.shape[1]))

  # Loop over rows in the data and sort them into the appropriate arrays
  for row in data_array:
    value = row[column_index]
    if 18 <= value <= 22:
      arr_18_22 = np.vstack([arr_18_22, row])
    elif 28 <= value <= 32:
      arr_28_32 = np.vstack([arr_28_32, row])
    elif 38 <= value <= 42:
      arr_38_42 = np.vstack([arr_38_42, row])
    else:
      arr_other = np.vstack([arr_other, row])

  # Return the sorted arrays
  return arr_18_22, arr_28_32, arr_38_42, arr_other


def sort_alpha_range(data_array, column_index):
  # Create empty arrays for each range
  arr_neg12_pos12 = np.empty((0, data_array.shape[1]))

  # Loop over rows in the data and sort them into the appropriate arrays
  for row in data_array:
    value = row[column_index]
    if -12 <= value <= 12:
      arr_neg12_pos12 = np.vstack([arr_neg12_pos12, row])

  # Return the sorted arrays
  return arr_neg12_pos12


def sort_beta(data_array, column_index):
  # Create empty arrays for each range
  arr_15 = np.empty((0, data_array.shape[1]))
  arr_30 = np.empty((0, data_array.shape[1]))

  # Loop over rows in the data and sort them into the appropriate arrays
  for row in data_array:
    value = row[column_index]
    if value == 15:
      arr_15 = np.vstack([arr_15, row])

    elif value == 30:
      arr_30 = np.vstack([arr_30, row])
  # Return the sorted arrays
  return arr_15, arr_30


def sort_J(data_array, column_index, min, max):
  # Create empty arrays for each range
  arr = np.empty((0, data_array.shape[1]))

  # Loop over rows in the data and sort them into the appropriate arrays
  for row in data_array:
    value = round(row[column_index], 2)  # round to two decimals
    if min - 0.01 <= value <= max - 0.01:
      arr = np.vstack([arr, row])

  # Return the sorted arrays
  return arr


def sort_J_bin(data_array, column_index):
    # get minimum and maximum values of J and round to closest 0.05
    J_min = round(np.min(data_array[:, column_index]) / 0.05) * 0.05
    J_max = round(np.max(data_array[:, column_index]) / 0.05) * 0.05
    J_bins = np.arange(J_min, J_max + 0.05, 0.05)
    
    # create arrays for each bin of J
    J_arrays = [np.empty((0, data_array.shape[1]), dtype=data_array.dtype) for i in range(len(J_bins))]
    
    # sort rows of data_array to closest J value and add to its bin of J
    for row in data_array:
        J_value = round(row[column_index] / 0.05) * 0.05

        bin_index = int(round((J_value - J_min) / 0.05))
        J_arrays[bin_index] = np.vstack([J_arrays[bin_index], row])
    
    # returns list of arrays for each bin of J
    return J_arrays



def sort_alpha_value(data, column_index):
  # Create empty arrays for each value
  arr_neg12 = np.empty((0, data.shape[1]))
  arr_neg10 = np.empty((0, data.shape[1]))
  arr_neg8 = np.empty((0, data.shape[1]))
  arr_neg6 = np.empty((0, data.shape[1]))
  arr_neg4 = np.empty((0, data.shape[1]))
  arr_neg2 = np.empty((0, data.shape[1]))
  arr_0 = np.empty((0, data.shape[1]))
  arr_2 = np.empty((0, data.shape[1]))
  arr_4 = np.empty((0, data.shape[1]))
  arr_6 = np.empty((0, data.shape[1]))
  arr_8 = np.empty((0, data.shape[1]))
  arr_10 = np.empty((0, data.shape[1]))
  arr_12 = np.empty((0, data.shape[1]))

  # Loop over rows in the data and sort them into the appropriate arrays
  for row in data:
    value = row[column_index]
    if value == -12:
      arr_neg12 = np.vstack([arr_neg12, row])
    elif value == -10:
      arr_neg10 = np.vstack([arr_neg10, row])
    elif value == -8:
      arr_neg8 = np.vstack([arr_neg8, row])
    elif value == -6:
      arr_neg6 = np.vstack([arr_neg6, row])
    elif value == -4:
      arr_neg4 = np.vstack([arr_neg4, row])
    elif value == -2:
      arr_neg2 = np.vstack([arr_neg2, row])
    elif value == 0:
      arr_0 = np.vstack([arr_0, row])
    elif value == 2:
      arr_2 = np.vstack([arr_2, row])
    elif value == 4:
      arr_4 = np.vstack([arr_4, row])
    elif value == 6:
      arr_6 = np.vstack([arr_6, row])
    elif value == 8:
      arr_8 = np.vstack([arr_8, row])
    elif value == 10:
      arr_10 = np.vstack([arr_10, row])
    elif value == 12:
      arr_12 = np.vstack([arr_12, row])

  # Return the sorted arrays
  return arr_neg12, arr_neg10, arr_neg8, arr_neg6, arr_neg4, arr_neg2, arr_0, arr_2, arr_4, arr_6, arr_8, arr_10, arr_12


# # split into propulsive and regenerative regimes based on value of current, 'I_M'
# data_propulsive, data_regen = filter_prop_regen(excel_path)

# # split propulsive and regenerative regimes into 20, 30, 40, and other m/s
# prop_18_22, prop_28_32, prop_38_42, prop_other = sort_Vinf(data_propulsive, 8)
# regen_18_22, regen_28_32, regen_38_42, regen_other = sort_Vinf(data_regen, 8)

# # sort based on alpha
# prop_V30 = sort_alpha(prop_28_32, 9)
# regen_V30 = sort_alpha(regen_28_32, 9)

# # some data goes missing between alpha and beta sorting

# # sort based on beta
# prop_V30_beta15, prop_V30_beta30 = sort_beta(prop_V30, 10)

# # sort based on J as specified per beta in reader
# prop_V30_beta15 = sort_J(prop_V30_beta15, 13, 0.55, 1.50)
# prop_V30_beta30 = sort_J(prop_V30_beta30, 13, 0.90, 2.10)

# # problem because we don't get the full range of J
# print(min(prop_V30_beta15[:, 13]))
# print(max(prop_V30_beta15[:, 13]))
# print(min(prop_V30_beta30[:, 13]))
# print(max(prop_V30_beta30[:, 13]))
