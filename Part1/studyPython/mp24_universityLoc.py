import folium
import pandas as pd

filePath = 'C:/Source/Mini-Projects/Part1/studyPython/university_locations.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl', header=None)
df_excel.columns = ['학교명', '주소', 'lng', 'lat']

# print(df_excel)
name_list = df_excel['학교명'].to_list()
addr_list = df_excel['주소'].to_list()
lng_list = df_excel['lng'].to_list()
lat_list = df_excel['lat'].to_list()

fmap = folium.Map(location=[37.553175, 126.989326], zoom_start = 10)

for i in range(len(name_list)):# 446
    if lng_list[i] != 0: # 위,경도값이 0이 아니면 출력 안된다.
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i],
                                icon=folium.Icon(color='blue'))
        marker.add_to(fmap)

fmap.save('./Korea_universities.html')