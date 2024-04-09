import numpy as np


def get_params_er4(nopa):
    people_affected_scale_er, people_affected_scale_trees, people_affected_scale_fct, people_affected_scale_dgl = nopa
    #print("This is the scenario for flooding in Emergency rooms. Please enter the values below. ")
    num_people_affected_er = 40
    #people_affected_scale_er = 2
    severity_of_damage_er = "ml1"
    severity_of_damage_scale_er = 4


    #print("This is the scenario for trees fell on the road. Please enter the values below. ")

    num_people_affected_trees = 80
    #people_affected_scale_trees = 3
    severity_of_damage_trees = "ml2"
    severity_of_damage_scale_trees = 5
    #print("Accroding to scale of importance (SOI) from table 6, the values are  ")
    #num_people_affected_soi = int(input("Please enter the vales for the NOPA;"))
    #damaged_area_soi = int(input("Please enter the vales for the DA:"))



    #print("This is the scenario for Fallen Cell Towers. Please enter the values below. ")

    num_people_affected_fct = 4000
    #people_affected_scale_fct = 8
    severity_of_damage_fct = "ll2"
    severity_of_damage_scale_fct = 3
    #print("Accroding to scale of importance (SOI) from table 6, the values are  ")
    #num_people_affected_soi = int(input("Please enter the vales for the NOPA;"))
    #damaged_area_soi = int(input("Please enter the vales for the DA:"))

      #print("This is the scenario for Damaged Gas lines. Please enter the values below. ")

    num_people_affected_dgl = 250
    #people_affected_scale_dgl = 4
    severity_of_damage_dgl = "hl3"
    severity_of_damage_scale_dgl = 9
    #print("Accroding to scale of importance (SOI) from table 6, the values are  ")
    #num_people_affected_soi = int(input("Please enter the vales for the NOPA;"))
    #damaged_area_soi = int(input("Please enter the vales for the DA:"))
    #values = [[round((num_people_affected_soi/num_people_affected_soi), 2), round((severity_of_damage_soi/num_people_affected_soi), 2)], [round((num_people_affected_soi/severity_of_damage_soi), 2), round((severity_of_damage_soi/severity_of_damage_soi), 2)]]

    values_4x4 = [[round((people_affected_scale_er/people_affected_scale_er), 2), round((people_affected_scale_er/people_affected_scale_trees), 2), round((people_affected_scale_er/people_affected_scale_fct), 2), round((people_affected_scale_er/people_affected_scale_dgl), 2)],

              [round((people_affected_scale_trees/people_affected_scale_er), 2), round((people_affected_scale_trees/people_affected_scale_trees), 2), round((people_affected_scale_trees/people_affected_scale_fct), 2), round((people_affected_scale_trees/people_affected_scale_dgl), 2)],

              [round((people_affected_scale_fct/people_affected_scale_er), 2), round((people_affected_scale_fct/people_affected_scale_trees), 2), round((people_affected_scale_fct/people_affected_scale_fct), 2), round((people_affected_scale_fct/people_affected_scale_dgl), 2)],

              [round((people_affected_scale_dgl/people_affected_scale_er), 2), round((people_affected_scale_dgl/people_affected_scale_trees), 2), round((people_affected_scale_dgl/people_affected_scale_fct), 2), round((people_affected_scale_dgl/people_affected_scale_dgl), 2)], 
              
              ]
    #print(values_4x4)
    return values_4x4



def square_matrix(matrix):
    return np.dot(matrix, matrix)


def create_matrix_from_values4(values_4x4):

    # Given list (assuming it has at least 16 elements; otherwise, fill the remainder with zeros or another placeholder)
    #values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    # Generating a 4x4 matrix from the list
    matrix_4x4 = np.array(values_4x4).reshape(4, 4)

    return matrix_4x4

# Example usage
#values = get_params_er()
#matrix = create_matrix_from_values(get_params_er())
#matrix3 = create_matrix_from_values(values3)
#print(matrix)



def normalize_matrix(matrix):
    norm = np.linalg.norm(matrix)
    if norm == 0:
        return matrix  # Return the original matrix if norm is 0 to avoid division by 0
    return matrix / norm


# # Input matrices
# print("Input matrix 1:")