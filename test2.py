from func_2 import create_matrix_from_values4, get_params_er4 # squared_part1, squared_part2 #, squared_part3
from func import  normalize_matrix, create_matrix_from_values, get_params_er, get_location_by_ip, load_excel, square_matrix, get_location_by_ip  #squared_part2, squared_part3
import pandas as pd
import numpy as np
import requests
import datetime, calendar, math

df = load_excel()
#df_sorted = df.sort_values(by='PRIORITY', ascending=False)
data_dict = {column: df[column].tolist() for column in df.columns}
names = []
nopa = []
sod = []
#print(df)
for i, items in data_dict.items():
    j = len(items)
    if i != "INSTANCES":
        #print(i, items)
        names.append(i)
        nopa.append(items[0])
        sod.append(items[1])
print(names)   
    # for pos in range(j):
    #     print(items[pos])
df = pd.DataFrame(list(zip(names, nopa, sod)),
                  columns = ["Names", "NOPA", "SOD"], index = None)

nopa_value = int(input("Number of People Affected(5): "))
sod_value = int(input("The Severity of Damage(2): "))

main_matrix = create_matrix_from_values(get_params_er(nopa_value,sod_value))
square_main_matrix = square_matrix(main_matrix)
woi = normalize_matrix((square_main_matrix))
print(woi[0])
print(woi)
matrix1 = create_matrix_from_values4(get_params_er4(nopa))
matrix2 = create_matrix_from_values4(get_params_er4(sod))



def normalize(matrix):


    # Extract individual elements from the matrix
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3]
    e, f, g, h = matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3]
    i, j, k, l = matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3]
    m, n, o, p = matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3]

    # Calculate the sum of all elements in the matrix
    total = np.sum(matrix)

    


    # Calculate the elements of the new matrix

    row1 = a + b + c + d
    row2 = e + f + g + h
    row3 = i + j + k + l
    row4 = m + n + o + p
    new_a = row1/total
    new_b = row2/total
    new_c = row3/total
    new_d = row4/total
    weight = [round(new_a, 2), round(new_b, 2),round(new_d, 2), round(new_c, 2)]
    # print("Print A = " + str(a))
    # print("Print B = " + str(b))
    
    norm_matrix.append(weight)
    print(round(new_a, 2), "++++++++", round(new_b, 2), "++++++++", round(new_c, 2), "++++++++", round(new_d, 2))
    # Return the squared matrix
    return norm_matrix

def draw_table_ahp(priority, names):
    #da_list, trees = priority
    daily_working_hours = 8
    column_names = ['INSTANCES', 'PRIORITY', 'RESILIENCE TIME(Hrs)', 'NO. OF PEOPLE REQUIRED', 'TOTAL TIME (Days)', 'START DATE', 'END DATE']
    rt_tfor = int(input("What is the Resilence Time for Trees fell on roads? (8): "))
    rt_fier = int(input("What is the Resilence Time for Flooding in emergency rooms? (4): "))
    rt_dgl = int(input("What is the Resilence Time for Damaged Gas lines? (6): "))
    rt_fct = int(input("What is the Resilence Time for Falling Cell Towers? (2): "))
    nopr_tfor = int(input("What is the Number of People needed for Trees fell on roads? (6): "))
    nopr_fier = int(input("What is the Number of People needed for Flooding in emergency rooms? (2): "))
    nopr_dgl = int(input("What is the Number of People needed for Damaged Gas lines? (3): "))
    nopr_fct = int(input("What is the Number of People needed for Falling Cell Towers? (2): "))
    today = datetime.datetime.today()
    
    resilience_time = [rt_fier, rt_tfor, rt_fct, rt_dgl]
    people_required = [nopr_fier, nopr_tfor, nopr_fct, nopr_dgl]
    total_time = []
    start_dates = []
    end_dates = []
    end_date = today

    names = np.array(names)
     
    resilience_time = np.array(resilience_time)
    people_required = np.array(people_required)
    priority =  np.array(priority)
    inds = priority.argsort()
    sorted_priority = inds[::-1]
    sorted_people_required = people_required[sorted_priority]
    sorted_resilience_time = resilience_time[sorted_priority]
    sorted_names = names[sorted_priority]
    
    

    for i in range(len(sorted_resilience_time)):
        total_days = (sorted_resilience_time[i] * sorted_people_required[i]) / daily_working_hours
        total_time.append(total_days)
        start_date = end_date
        start_dates.append(start_date)
        
        # Calculate the end date based on the floor of total_days for the current task
        end_date = start_date + datetime.timedelta(days=math.floor(total_days))
        end_dates.append(end_date)


    total_time = np.array(total_time) 
    sorted_total_time = total_time[sorted_priority]
    #print("Total time", total_time)
    # Create the DataFrame
    df = pd.DataFrame(list(zip(sorted_names, priority[sorted_priority], sorted_resilience_time, sorted_people_required, total_time, start_dates, end_dates)),
                  columns = column_names, index = None)
     
    
    df.to_excel('test2.xlsx', index=False)
     # Display the DataFrame
    print(df)




def calculate_priority_vector(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvector = eigenvectors[:, np.argmax(np.real(eigenvalues))]
    priority_vector = np.real(max_eigenvector / np.sum(max_eigenvector))
    return priority_vector
    # print("round",round(priority_vector[0],2))
    # print ("Priority:", priority_vector)

norm_matrix = []
squared_part1 = square_matrix(matrix1)
squared_part2 = square_matrix(matrix2)

normalize(squared_part1)
#print("This is the best of all ")
normalize(squared_part2)

#normalize(squared_part3)
get_location_by_ip()
for_people_affected = calculate_priority_vector(squared_part1)
for_severity_damage = calculate_priority_vector(squared_part2)
#print("PA", for_people_affected[0])

#print(norm_matrix[0][0] + norm_matrix[0][1])

###

# ans_da_pre = round(((norm_matrix[1][0] * norm_matrix[0][1]) + (norm_matrix[2][0] * norm_matrix[0][0])),3)
# ans_da = round(ans_da_pre,2)
# ans_tree = round(((norm_matrix[1][1] * norm_matrix[0][1]) + (norm_matrix[2][1] * norm_matrix[0][0])), 2)
# nopa_list = [norm_matrix[0][1], norm_matrix[0][0], (norm_matrix[0][0] + norm_matrix[0][1])]
# da_list = [norm_matrix[1][0], norm_matrix[2][0], ans_da]
# if ans_tree > (1 - ans_da):
#     ans_tree = (1 - ans_da)
# trees = [norm_matrix[1][1], norm_matrix[2][1], ans_tree]
# draw_table_ahp(nopa_list, da_list, trees)
###

def calculate_priority(for_people_affected, for_severity_damage, woi):
    #print (norm_matrix)
    woi_er = (for_people_affected[0] * woi[0][0]) + (for_severity_damage[0] * woi[0][1])
    woi_road= (for_people_affected[1] * woi[0][0]) + (for_severity_damage[1] * woi[0][1])
    woi_tower = (for_people_affected[2] * woi[0][0]) + (for_severity_damage[2] * woi[0][1] ) 
    woi_gas = (for_people_affected[3] * woi[0][0]) + (for_severity_damage[3] * woi[0][1])
    #Show the result for th
    return [round(woi_er, 9), round(woi_road, 9), round(woi_tower, 9), round(woi_gas, 9)]
    
#print(ans_tree)
#print(ans_da)
result = calculate_priority(for_people_affected, for_severity_damage, woi)
draw_table_ahp(result, names)
#print(result)