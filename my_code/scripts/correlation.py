import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# Load example dataset
file_path1 = os.path.join("excel_files", "hpeiros_new.xlsx")
df1 = pd.read_excel(file_path1)
names = df1.loc[:,['CODENAME']].drop_duplicates()
file_path3 = os.path.join("excel_files", "geocode synopsis EG 21_12.xlsx")
synopsis = pd.read_excel(file_path3, sheet_name='data_full')
merge = names.merge(synopsis, on = 'CODENAME' , how = 'inner')

#merge['education_years'] = pd.to_numeric(merge['education_years'], errors='coerce')
numeric_columns = merge.select_dtypes(include=[np.number])
# Calculate correlation matrix
correlation_matrix = numeric_columns.corrwith(merge['visit']).sort_values(ascending=False)
# Plot correlation matrix as heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix.to_frame(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Iris Dataset")
plt.savefig('education.png')
plt.show()
