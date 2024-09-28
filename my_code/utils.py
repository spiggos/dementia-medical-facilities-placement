import io
import os 
import pandas as pd
import numpy as np
import googlemaps
from polyline import decode as poly_decode
from pulp import*

def excel_maker(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print(f"Το αρχείο {file_path} δεν βρέθηκε.")
    except pd.errors.ParserError:
        print("Invalid excel file format.")


def adjust_coordinates(column):
    coord_list = []

    for coord in column:
        digit_count = len(str(coord))
        
        if digit_count == 10:
            adjusted_coord = coord * pow(10, -8)
        elif digit_count == 9:
            adjusted_coord = coord * pow(10, -7)
        elif digit_count == 8:
            adjusted_coord = coord * pow(10, -6)
        else:
            adjusted_coord = coord  # Μπορείς να χειριστείς άλλες περιπτώσεις αν χρειάζεται
        
        coord_list.append(adjusted_coord)
    
    return coord_list


def get_distance(api_key, start, end):
    gmaps = googlemaps.Client(key=api_key)
    # Request directions
    directions_result = gmaps.directions(start, end, mode="driving")
    polyline = directions_result[0]['overview_polyline']['points']
    decoded_polyline = poly_decode(polyline)
    # Extract the distance
    distance = directions_result[0]['legs'][0]['distance']['text']
    distance = distance.replace(' km', '')
    distance = float(distance)

    return distance, decoded_polyline


def get_values_by_area(areas, df, column_name):
    values = []  # Δημιουργία λίστας για να αποθηκεύσεις τις τιμές
    
    for area in areas: 
        filtered_df = df[df['house'] == area]  # Φιλτράρισμα του DataFrame με βάση την περιοχή
        unique_values = filtered_df[column_name].unique()  # Λήψη μοναδικών τιμών από την καθορισμένη στήλη
        
        if len(unique_values) > 0:
            value = unique_values[0]  # Πάρε τη πρώτη τιμή
            convert = float(value)  # Μετατροπή σε float
            values.append(convert)  # Προσθήκη στη λίστα
            
            # Για debug, αν χρειάζεται:
            # print(f"Area: {area}, {column_name}: {value}")
    
    return values  # Επιστροφή της λίστας με τις τιμές


def normalized_factor(MAX,MIN,values_list):
    normalized_factor= list()
    if MAX != MIN :
        if values_list:
            normalized_factor = [(li-MIN)/(MAX-MIN) for li in values_list]
    return normalized_factor
        

def apply_weights(weights:list, normalized_factor1:list,normalized_factor2:list,normalized_factor3:list,normalized_factor4:list,normalized_factor5:list):
    a1 =[number*weights[0] for number in normalized_factor1]
    a2 =[number*weights[1] for number in normalized_factor2]
    a3 =[number*weights[2] for number in normalized_factor3]
    a4 =[number*weights[3] for number in normalized_factor4]
    a5 =[number*weights[4] for number in normalized_factor5]

    result = [number1+number2+number3+number4+number5 for number1,number2,number3,number4,number5 in zip(a1,a2,a3,a4,a5)]

    return result


def solve_p_median(p, candidate_location, non_median, distance, result):
    # Set the working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    X = LpVariable.dicts('X',(candidate_location),0,1,LpBinary)
    Y = LpVariable.dicts('Y',[(area,centers) for area in non_median for centers in candidate_location],0,1,LpBinary)

    #2D
    allocation = np.array(list(Y.values())).reshape(40,12)
    D = np.reshape(distance, (40,12))
    demand=np.array(result).reshape(40,1)

    #FORMULATION
    # MODEL: MINIMIZATION problem
    model = LpProblem('P Median', LpMinimize)

    #OBJECTIVE FUNCTION
    obj_func = lpSum([demand[i]*lpDot(D[i], allocation[i]) for i in range(40)])
    model += obj_func

    #CONSTRAINTS
    model += lpSum(X[j] for j in candidate_location) == p
    for i in non_median:
        model += lpSum(Y[i,j] for j in candidate_location) == 1

    for i in non_median:
        for j in candidate_location:
            model +=  Y[i,j] <= X[j]

    #Δημιουργεία ενός file για το LP-model 
    output_folder = 'lp_files'
    os.makedirs(output_folder, exist_ok=True)
    output_filename = 'p-median.lp'

    output_path = os.path.join(output_folder, output_filename)
    with io.open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(model))

    model.solve()

    #FORMAT OUTPUT
    print("Objective: ",value(model.objective))
    print(' ')

    return model