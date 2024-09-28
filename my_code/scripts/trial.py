import pandas as pd

# Διαβάζουμε το αρχείο Excel
df = pd.read_excel('combinations.xlsx')  # Αντικατέστησε το 'weights.xlsx' με το όνομα του αρχείου σου

# Μετατροπή των δεδομένων σε λίστα
data_list = df.values.tolist()

# Κανονικοποιημένοι αριθμοί (Παράδειγμα τιμών)
normalized_factor1 = [0.5, 0.6, 0.7]
normalized_factor2 = [0.4, 0.5, 0.6]
normalized_factor3 = [0.3, 0.4, 0.5]
normalized_factor4 = [0.2, 0.3, 0.4]
normalized_factor5 = [0.1, 0.2, 0.3]

def apply_weights(weights, nf1, nf2, nf3, nf4, nf5):
    a1 = [number * weights[0] for number in nf1]
    a2 = [number * weights[1] for number in nf2]
    a3 = [number * weights[2] for number in nf3]
    a4 = [number * weights[3] for number in nf4]
    a5 = [number * weights[4] for number in nf5]    

    result = [number1 + number2 + number3 + number4 + number5
              for number1, number2, number3, number4, number5
              in zip(a1, a2, a3, a4, a5)]
    
    return result

results = []
for weights in data_list:
    result = apply_weights(weights, normalized_factor1, normalized_factor2, normalized_factor3, normalized_factor4, normalized_factor5)
    results.append(result)

    results_df = pd.DataFrame(results, columns=['Result1', 'Result2', 'Result3'])

# Αποθήκευση αποτελεσμάτων σε αρχείο CSV
results_df.to_excel('results.xlsx', index=False)