from func import create_matrix_from_values, find_next_corresponding_value, square_matrix, get_location_by_ip, get_params_er
import pandas as pd
import numpy as np
import requests
import datetime, math
import calendar



pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


organization = input("What is the name of your orgaization: ")
print(f"Welcome to {organization}'s DMS \nBelow is your current location.\n")
get_location_by_ip()
print(f"Please complete the information below accurately \n")


print("This is the scenario for flooding in Emergency rooms. Please enter the values below. \n")
num_people_affected_er = int(input("Please enter the number of people affected in 40: "))
people_affected_scale_er = find_next_corresponding_value('nopa.xlsx', 0, num_people_affected_er) #2
#print(people_affected_scale_er)
damaged_area_er = int(input("Please enter the size of the damage area affected (without unit(15)): "))
damaged_area_scale_er = find_next_corresponding_value('damaged_area_scale.xlsx', 0, damaged_area_er)  #4

print(f"\nThis is the scenario for trees fell on the road. Please enter the values below. ")
num_people_affected_trees = int(input("Please enter the number of people affected in 80: "))
people_affected_scale_trees = find_next_corresponding_value('nopa.xlsx', 0, num_people_affected_trees) #3
damaged_area_trees = int(input("Please enter the number of people affected 25: "))
damaged_area_scale_trees = find_next_corresponding_value('damaged_area_scale.xlsx', 0, damaged_area_trees) #5

print("Accroding to scale of importance (SOI) from table 6, the values are  ")
""" No. of people affected => 1
    Damaged Area (m^2) => 2
    Time taken for resilience => 3
    Severity of damage => 4
"""
num_people_affected_soi = find_next_corresponding_value('damaged_area_scale.xlsx', 0, 1)  
damaged_area_soi = find_next_corresponding_value('damaged_area_scale.xlsx', 0, 2)


matrix1 = create_matrix_from_values(get_params_er(damaged_area_soi, num_people_affected_soi))
# print("Input matrix 2:")
matrix2 = create_matrix_from_values(get_params_er(people_affected_scale_er,people_affected_scale_trees))
# print("Input matrix 3:")
matrix3 = create_matrix_from_values(get_params_er(damaged_area_scale_er, damaged_area_scale_trees))


# # Now square the concatenated matrix
squared_part1 = square_matrix(matrix1)
squared_part2 = square_matrix(matrix2)
squared_part3 = square_matrix(matrix3)



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

def draw_table_ahp(priority):
    da_list, trees = priority
    daily_working_hours = 8
    column_names = ['INSTANCES', 'PRIORITY', 'RESILIENCE TIME(Hrs)', 'NO. OF PEOPLE REQUIRED', 'TOTAL TIME (Days)', 'START DATE', 'END DATE']
    rt_tfor = int(input("What is the Resilence Time for Trees fell on roads? (8): "))
    rt_fier = int(input("What is the Resilence Time for Flooding in emergency rooms? (4): "))
    
    nopr_tfor = find_next_corresponding_value('resilence_time_scale.xlsx', 0, rt_tfor) #2
    print(f"The number of people required is {nopr_tfor}")
    nopr_fier = find_next_corresponding_value('resilence_time_scale.xlsx', 0, rt_fier) #3
    print(f"The number of people required is {nopr_fier}")
    today = datetime.datetime.today()
    # day = datetime.datetime.today().day
    # month = datetime.datetime.today().month
    # month_name = calendar.month_name[datetime.datetime.today().month]
    # day_name = calendar.day_name[datetime.datetime.today().day]
    #print(f'Today\'s date is {today}\n{day_name}, {month_name}')
    total_time = (rt_tfor*nopr_tfor)/daily_working_hours
    total_time_er = (rt_fier*nopr_fier)/daily_working_hours
    #print (total_time)
    end_day_tfor = today + datetime.timedelta(days=math.floor(total_time))
    end_day_fier = end_day_tfor + datetime.timedelta(days=math.floor(total_time))
     # Initialize the data for the DataFrame
    #print(trees)
    data = [
             ['Trees fell on roads', round(trees[2], 5), rt_tfor, nopr_tfor, total_time, today, end_day_tfor],
             ['Flooding in emergency rooms', da_list[2], rt_fier, nopr_fier, total_time_er, end_day_tfor, end_day_fier]
     ]
    #print(data)
     # Create the DataFrame
    df = pd.DataFrame(data, columns=column_names)
    df.to_excel('test1.xlsx', index=False)
     # Display the DataFrame
    print(df)



# def calculate_priority_vector(matrix):
#     eigenvalues, eigenvectors = np.linalg.eig(matrix)
#     max_eigenvector = eigenvectors[:, np.argmax(np.real(eigenvalues))]
#     priority_vector = np.real(max_eigenvector / np.sum(max_eigenvector))
#     print(priority_vector)
#     return priority_vector


norm_matrix = []
normalize(squared_part1)
normalize(squared_part2)
normalize(squared_part3)

#print(norm_matrix)

def calculate_priority(norm_matrix):
    #print (norm_matrix)
    ans_da = (norm_matrix[0][1] * norm_matrix[1][0]) + (norm_matrix[2][0] * norm_matrix[0][0]) 
    ans_tree = (norm_matrix[1][1] * norm_matrix[0][1]) + (norm_matrix[2][1] * norm_matrix[0][0])
    nopa_list = [norm_matrix[0][1], norm_matrix[0][0], (norm_matrix[0][0] + norm_matrix[0][1])]
    da_list = [norm_matrix[1][0], norm_matrix[2][0], ans_da]
    #print(f'{ans_da}, \n {ans_tree}, \n{nopa_list}\n {da_list}')
    if ans_tree > (1 - ans_da):
        ans_tree = (1 - ans_da)
    trees = [norm_matrix[2][0], norm_matrix[2][1], ans_tree]
    print(da_list, trees)
    return da_list, trees
#print(ans_tree)
#print(ans_da)
result = calculate_priority(norm_matrix)
draw_table_ahp(result)