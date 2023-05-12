import pandas as pd
import numpy as np
from pathlib import Path

excel_path = Path(r'/home/jasper/Documents/data_group_c09/Data_C09_Integral.xls')

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
        value = round(row[column_index],4) # round to two decimals
        # value = row[column_index]
        if value == 0.5465:
            print("Found you")
        if min-0.01 <= value <= max-0.01:
            arr = np.vstack([arr, row])

    # Return the sorted arrays
    return arr

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



