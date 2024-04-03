from func_2 import squared_part1, squared_part2 #, squared_part3
from func import get_location_by_ip  #squared_part2, squared_part3
import pandas as pd
import numpy as np
import requests

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
    print(round(new_d, 2), "++++++++", round(new_c, 2))
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
