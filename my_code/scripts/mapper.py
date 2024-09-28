import folium
import os
import pandas as pd
import webbrowser

file_path1 = os.path.join("excel_files", "hpeiros_new.xlsx")
df1 = pd.read_excel(file_path1)
people_coords = df1.loc[:,['longtitude','latitude']].drop_duplicates()
file_path2 = os.path.join("excel_files", "hpeiros_all_centers.xlsx")
df2 = pd.read_excel(file_path2)
center_coords = df2.loc[:,['all_centers_long','all_centers_lat']].drop_duplicates()

long_list= list()
lat_list= list()
for logntitude in people_coords['longtitude']:
    digit_counts = len(str(logntitude))
    if digit_counts==10:
        long = logntitude*pow(10,-8)
        long_list.append(long)
    if digit_counts==9:
        long = logntitude*pow(10,-7)
        long_list.append(long)
    if digit_counts==8:
        long = logntitude*pow(10,-6)
        long_list.append(long)

for latitude in people_coords['latitude']:
    digit_counts2 = len(str(latitude))
    if digit_counts2==10:
        lat = latitude*pow(10,-8)
        lat_list.append(lat)
    if digit_counts2==9:
        lat = latitude*pow(10,-7)
        lat_list.append(lat)
    if digit_counts2==8:
        lat = latitude*pow(10,-6)
        lat_list.append(lat)

#Δημιουργεία excel απο το lat_list και long_list 
people_geo= pd.DataFrame({'longtitude':long_list,'latitude':lat_list})

map = folium.Map(

    location=[38.2745,23.8103],
    tiles='openstreetmap',
    zoom_start=7,
)

#for index, row in people_geo.iterrows():
#    folium.Marker(
#        location=[row['latitude'], row['longtitude']],
#        icon=folium.Icon(prefix="fa", icon="home")
#    ).add_to(map)

for index, row in center_coords.iterrows():
    folium.Marker(  
                    location=[row['all_centers_lat'], row['all_centers_long']],
                    icon=folium.Icon(color='green',icon='medkit',prefix="fa")
                ).add_to(map) 
map.save('html_files/centers_map.html')
