from func_2 import create_matrix_from_values4, get_params_er4 # squared_part1, squared_part2 #, squared_part3
from func import create_matrix_from_values, get_params_er, get_location_by_ip, load_excel, square_matrix, get_location_by_ip  #squared_part2, squared_part3
import pandas as pd
import numpy as np
import requests

df = load_excel()
#df_sorted = df.sort_values(by='PRIORITY', ascending=False)
data_dict = {column: df[column].tolist() for column in df.columns}
#print(data_dict)
nopa = []
sod = []
#print(df)
for i, items in data_dict.items():
    j = len(items)
    
    if i != "INSTANCES":
        #print(i, items)
        nopa.append(items[0])
        sod.append(items[1])
    
    # for pos in range(j):
    #     print(items[pos])
#print(nopa, sod)
nopa_value = int(input("Number of People Affected(5): "))
sod_value = int(input("The Severity of Damage(2)"))

main_matrix = create_matrix_from_values(get_params_er(nopa_value,nopa_value))

print(main_matrix)

matrix1 = create_matrix_from_values4(get_params_er4(nopa))
matrix2 = create_matrix_from_values4(get_params_er4(sod))
#print (matrix1)
#print (matrix2)


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

def draw_table_ahp(woi_list, da_list, trees):

        
    # Initialize the data for the DataFrame
    data = {'': ['For No of People affected', 'For Damaged Area', 'Sum of weights of importance'],
            'Weight of Importance': woi_list,  # Leaving spaces as placeholders
            'Flooding in emergency rooms': da_list,
            'Trees fell on roads': trees
            }

    # Create the DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    print(df)



def calculate_priority_vector(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvector = eigenvectors[:, np.argmax(np.real(eigenvalues))]
    priority_vector = np.real(max_eigenvector / np.sum(max_eigenvector))
    print("round",round(priority_vector[0],2))
    print ("Priority:", priority_vector)

norm_matrix = []
squared_part1 = square_matrix(matrix1)
squared_part2 = square_matrix(matrix2)

normalize(squared_part1)
#print("This is the best of all ")
normalize(squared_part2)

#normalize(squared_part3)
get_location_by_ip()
calculate_priority_vector(squared_part1)
calculate_priority_vector(squared_part2)
print(norm_matrix)

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