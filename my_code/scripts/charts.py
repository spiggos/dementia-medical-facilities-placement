import pandas as pd
import plotly.express as px 

# Φόρτωση δεδομένων από το Excel αρχείο
df = pd.read_excel('excel_files/edges.xlsx')
df['centers_color'] = df['centers']

# Δημιουργία ενός διαδραστικού διαγράμματος Sunburst με καθορισμένα χρώματα ανά κέντρο υγείας
fig = px.sunburst(df,path=['centers','non_median'], 
                  color='centers_color',
                  title='Συνδέσεις Περιοχών με Κέντρα Υγείας στην Ήπειρο',
                  color_discrete_sequence=px.colors.qualitative.Plotly) # Χρησιμοποιούμε προκαθορισμένη χρωματική παλέτα 

# Προσθήκη υπομνήματος
fig.update_layout(
    legend_title_text='Κέντρα Υγείας',
    legend=dict(
        title='Κέντρα Υγείας',
        itemsizing='constant'
    )
)

# Αποθήκευση του διαδραστικού διαγράμματος σε HTML αρχείο
fig.write_html('html_files/area_health_centers_sunburst.html')

# Εμφάνιση του διαγράμματος
fig.show()
