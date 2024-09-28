import itertools
import pandas as pd
import numpy as np

# Ορισμός των τιμών για κάθε μεταβλητή
visit =  np.arange(0.1, 0.9, 0.05).tolist() 
neuro =  np.arange(0.1, 0.9, 0.05).tolist() 
dd =  np.arange(0.1, 0.9, 0.05).tolist() 
otherd =  np.arange(0.1, 0.9, 0.05).tolist() 
age =  np.arange(0.1, 0.9, 0.05).tolist() 

# Δημιουργία όλων των πιθανούς συνδυασμών
combinations = list(itertools.product(
    visit,
    neuro,
    dd,
    otherd,
    age
))

# Φιλτράρισμα των συνδυασμών που πληρούν την συνθήκη
valid_combinations = [
    combo for combo in combinations
    if round(sum(combo), 10) == 1.0  # Στρογγυλοποίηση για αποφυγή αριθμητικών σφαλμάτων
]

df = pd.DataFrame(valid_combinations, columns=[
    'visit',
    'neuro',
    'dd',
    'od',
    'age'
])


# Αποθήκευση
df.to_excel('excel_files/combinations.xlsx', index=False)


