import numpy as np
import requests
import pandas as pd

def get_params_er(num_people_affected_soi, damaged_area_soi):
    #print("This is the scenario for flooding in Emergency rooms. Please enter the values below. \n")
    num_people_affected_er = 40
    people_affected_scale_er = 2
    damaged_area_er = 15
    damaged_area_scale_er = 4

    #print(f"\nThis is the scenario for trees fell on the road. Please enter the values below. ")

    num_people_affected_trees = 80 #input("Please enter the number of people affected in 80: ")
    people_affected_scale_trees = 3 #input("Please enter the number of people affected 3: ")
    damaged_area_trees = 25 #input("Please enter the number of people affected 25: ")
    damaged_area_scale_trees = 5 #input("Please enter the scale of damaged area 5: ")
    
    #print("Accroding to scale of importance (SOI) from table 6, the values are  ")
    #num_people_affected_soi = int(input("Please enter the vales for the NOPA;"))
    #damaged_area_soi = int(input("Please enter the vales for the DA:"))

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

# Example usage
#values = get_params_er()
#matrix = create_matrix_from_values(get_params_er())
#matrix3 = create_matrix_from_values(values3)
#print(matrix)

# def normalize_matrix(matrix):
#     norm = np.linalg.norm(matrix)
#     if norm == 0:
#         return matrix  # Return the original matrix if norm is 0 to avoid division by 0
#     return matrix / norm
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

# # Input matrices
# # print("Input matrix 1:")
matrix1 = create_matrix_from_values(get_params_er(3,5))
# print("Input matrix 2:")
matrix2 = create_matrix_from_values(get_params_er(2,3))
# print("Input matrix 3:")
matrix3 = create_matrix_from_values(get_params_er(4,5))


# # Now square the concatenated matrix
squared_part1 = square_matrix(matrix1)
squared_part2 = square_matrix(matrix2)
squared_part3 = square_matrix(matrix3)

