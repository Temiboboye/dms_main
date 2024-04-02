from func import squared_part1, squared_part2, squared_part3
import pandas as pd
import numpy as np
import requests
import datetime, math
import calendar


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def normalize(matrix):
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

def draw_table_ahp(da_list, trees):

    column_names = ['INSTANCES', 'PRIORITY', 'RESILIENCE TIME(Hrs)', 'NO. OF PEOPLE REQUIRED', 'TOTAL TIME (Days)', 'START DATE', 'END DATE']
    rt_tfor = int(input("What is the Resilence Time for Trees fell on roads? (8): "))
    rt_fier = int(input("What is the Resilence Time for Flooding in emergency rooms? (4): "))
    nopr_tfor = int(input("What is the Number of People needed for Flooding in emergency rooms? (2): "))
    nopr_fier = int(input("What is the Number of People needed for Flooding in emergency rooms? (3): "))
    today = datetime.datetime.today()
    month = calendar.month_name[datetime.datetime.today().month]
    print(month)
    
    end_day_tfor = today + datetime.timedelta(days=math.floor(rt_tfor/nopr_tfor))
    end_day_fier = end_day_tfor + datetime.timedelta(days=math.floor(rt_fier/nopr_fier))
     # Initialize the data for the DataFrame
    data = [
             ['Trees fell on roads', trees[2] , rt_tfor, nopr_tfor, rt_tfor/nopr_tfor, today, end_day_tfor], # Leaving spaces as placeholders
             ['Flooding in emergency rooms', da_list[2], rt_fier, nopr_fier, rt_fier/nopr_fier, end_day_tfor, end_day_fier]
     ]
    #print(data)
     # Create the DataFrame
    df = pd.DataFrame(data, columns=column_names)
    df.to_excel('test1.xlsx', index=False)
     # Display the DataFrame
    #print(df)


#Location API 
def get_location_by_ip():
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    print(data)
    # Extract required information
    post_code = data['postal']
    long, lat = data['loc'].split(',')
    city = data['city']
    region = data['region']
    country = data['country']

    # Construct standard address format
    address_format = f"{city}, {region}, {country}, Postal Code: {post_code}"
    
    # Print the address in standard format
    print("Your IP location info:", address_format)
    
    # Return postal code and longitude as variables
    return post_code, long, lat, city, region

def calculate_priority_vector(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvector = eigenvectors[:, np.argmax(np.real(eigenvalues))]
    priority_vector = np.real(max_eigenvector / np.sum(max_eigenvector))
    print(priority_vector)
    return priority_vector


norm_matrix = []
normalize(squared_part1)

# #print("This is the best of all ")
normalize(squared_part2)

normalize(squared_part3)
#calculate_priority_vector(squared_part3)
#print(norm_matrix)
#print(norm_matrix[0][0] + norm_matrix[0][1])


#print(priority_vector)
ans_da_pre = (norm_matrix[1][0] * norm_matrix[0][1]) + (norm_matrix[2][0] * norm_matrix[0][0]) 
ans_da = ans_da_pre
ans_tree = (norm_matrix[1][1] * norm_matrix[0][1]) + (norm_matrix[2][1] * norm_matrix[0][0])
nopa_list = [norm_matrix[0][1], norm_matrix[0][0], (norm_matrix[0][0] + norm_matrix[0][1])]
da_list = [norm_matrix[1][0], norm_matrix[2][0], ans_da]
if ans_tree > (1 - ans_da):
    ans_tree = (1 - ans_da)
trees = [norm_matrix[2][0], norm_matrix[2][1], ans_tree]
#print(ans_tree)
#print(ans_da)
draw_table_ahp(da_list, trees)