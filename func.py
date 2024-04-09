import numpy as np
import requests
import pandas as pd




def find_next_corresponding_value(file_path, lookup_column, input_value):
    """
    Finds the next corresponding value in an Excel file based on the specified rules.
    
    Parameters:
    - file_path: str, path to the Excel file
    - lookup_column: int or str, index or name of the column to look up the input_value
    - input_value: float, the value to find the corresponding value for
    
    Returns:
    - The found corresponding value from the next row based on the rules, or None if not found.
    """
    try:
        df = pd.read_excel(file_path)
        
        # Ensure lookup_column is valid
        if isinstance(lookup_column, int):
            lookup_series = df.iloc[:, lookup_column]
        elif isinstance(lookup_column, str):
            lookup_series = df[lookup_column]
        else:
            print("Invalid lookup_column provided.")
            return None
        
        # Ensure the DataFrame is sorted by the lookup column
        df_sorted = df.sort_values(by=lookup_series.name)
        print(df_sorted)
        # Find the index of the row that meets the condition
        suitable_index = df_sorted.index[df_sorted[lookup_series.name] >= input_value].min()
        #print(suitable_index)
        # If the input value is less than the first entry, consider the first entry's value
        if suitable_index == df_sorted.index.min() and input_value <= df_sorted.iloc[0][lookup_column]:
            return df_sorted.loc[suitable_index].iloc[1] #df_sorted.iloc[0].iloc[1]
        elif suitable_index > df_sorted.index.min():
            # Return the corresponding value from the next row
            return df_sorted.loc[suitable_index].iloc[1]
        else:
            return None
    except ValueError:
        # This handles the case where no rows meet the condition
        return None
    except Exception as e:
        print(f"Error processing the file: {e}")
        return None


def get_params_er(num_people_affected_soi, damaged_area_soi):

    values = [[(num_people_affected_soi/num_people_affected_soi), (damaged_area_soi/num_people_affected_soi)], [num_people_affected_soi/damaged_area_soi, (damaged_area_soi/damaged_area_soi)]]

    return values



def square_matrix(matrix):
    return np.dot(matrix, matrix)

def input_matrix(size=(2, 2)):
    
    matrix = np.zeros(size)  # Initialize a matrix of zeros with the given size.
    for i in range(size[0]):  # Loop over rows
        for j in range(size[1]):  # Loop over columns
            # Ask the user to input the element at position (i, j)
            matrix[i, j] = float(input(f"Enter element [{i}, {j}]: "))
    return matrix

def create_matrix_from_values(values):
    
    # Convert the list of lists into a numpy array
    matrix = np.array(values)
    return matrix

def normalize_matrix(matrix):
    norm_matrix = []
    # matrix is a 2x2 matrix represented as [[a, b], [c, d]]

    # Extract individual elements from the matrix
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]

    # Calculate the sum of all elements in the matrix
    #total = a + b + c + d
    total = np.sum(matrix)
    row_total = a + c


    # Calculate the elements of the new matrix

    added = a + b
    bdded = c + d
    new_c = added/total
    new_d = bdded/total
    weight = [new_d, new_c]
    # print("Print A = " + str(a))
    # print("Print B = " + str(b))
    
    norm_matrix.append(weight)
    #print(new_c , " ++++++ ", new_d)
    # Return the squared matrix
    return norm_matrix

def load_excel():
    filename= input("Please enter yor file name (without xls):")
    # Load the task data from the provided Excel file
    file_path = f'{filename}.xlsx'  # Adjust based on the actual file path
    df = pd.read_excel(file_path)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    # Assuming the DataFrame has columns: 'Task', 'Priority', 'Resilience Time', 'People Required'
    # Sort tasks by Priority
    
    return df

#Location API 
def get_location_by_ip():
    
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    #print("IP Address", data)
    # Extract required information
    post_code = data['postal']
    long, lat = data['loc'].split(',')
    city = data['city']
    region = data['region']
    country = data['country']
    long,lat = data['loc'].split(',') #: '52.5855,-2.1230

    # Construct standard address format
    address_format = f"{city}, {region}, {country}, {post_code} \nLongitude: {long}, Latitude: {lat}"
    
    # Print the address in standard format
    print("Here is your current location", address_format)
    
    # Return postal code and longitude as variables
    return address_format




