# -*- coding: utf-8 -*-

"""

Created on Wed Aug 17 14:41:37 2022

 

@author: Mursal.Saleem

"""

#%% Import libraries

import pandas as pd
import folium
from sklearn.preprocessing import LabelEncoder
from scipy.spatial import ConvexHull

 

#%% Read file

property=pd.read_excel("Data/zameen-property-data.xlsx")
property = property[property.city == "Karachi"]
property = property[property.location.isin(['DHA Defence', 
                                             'Clifton',
                                             'Korangi'])]
# selected 10 areas just for making it breif for making clusters
# because we will have to specify each cluster name in folium
hospitals=pd.read_excel("Data/Karachi Hospitals.xlsx")

property.info()
hospitals.info()

property["location_n"] = LabelEncoder().fit_transform(property["location"])
# in order to create numeric values later to be used
#%% Create Map

 

def create_map(hsp,prt):

    m = folium.Map(location=[hsp.Latitude.mean(), hsp.Longitude.mean()], zoom_start=11)   
    
######################################################################################

    for _, row in hsp.iterrows():
        folium.Marker(
            location= [row['Latitude'],row['Longitude']],
            popup= str(row['Hospital Name']),
            #when you'll click on the icon whatever you want to see - tooltip
            size = (10,10),
            #icon = folium.Icon(color = cluster_color1, icon = "fa-hospital-o", prefix = "fa")
            icon = folium.CustomIcon('picture/hospital.png', icon_size= (30,30))
            #you can add any picture here with CustomIcon, other wise use folium.icon above           
            ).add_to(m)

#######################################################################################

    for _, x in property.iterrows():
        if x['location_n'] == 0:
            cluster_color = 'red'
        elif x['location_n'] == 1:
            cluster_color = 'green'      
        else:
            cluster_color = 'black'

         #if you dont want clusters remove the if else statements


        folium.CircleMarker(
            location = [x['latitude'], x['longitude']],
            popup= (str(x["latitude"]) + ", " + str(x["longitude"])),
            radius = 3,
            #change radius if you want to change circel size          
            color = cluster_color,
            fill = True,
            fill_color = cluster_color
            ).add_to(m)



###################################################################################

    #all of the below code is for the lines cornered for the clusters   
    #the below is for making it interactive and giving names for each cluster
    #--as per original
    layer1 = folium.FeatureGroup(name= '<u><b>DHA Defence</b></u>',show= True)
    m.add_child(layer1)
    layer2 = folium.FeatureGroup(name= '<u><b>Korangi</b></u>',show= True)
    m.add_child(layer2)
    layer3 = folium.FeatureGroup(name= '<u><b>Clifton</b></u>',show= True)
    m.add_child(layer3)

    

    layer_list = [layer1,layer2,layer3]
    color_list = ['green','black','red']

    #change layers as per your number of clusters

    

    for g in property['location_n'].unique():
        latlon_cut = property[property['location_n'] == g].iloc[: , 8:10]
        print(latlon_cut.info())
        hull = ConvexHull(latlon_cut.values)
        print(hull)
        Lat = latlon_cut.values[hull.vertices, 0]
        print(Lat)
        Lon = latlon_cut.values[hull.vertices, 1]
        print(Lon)
        cluster = pd.DataFrame({'latitude':Lat,'longitude':Lon }) 
        print(cluster)    
        area = list(zip(cluster['latitude'],cluster['longitude']))
        print(area)
        list_index = g-1 # (minus 1 to get the same index if you have numbered clusters)
        lay_cluster = layer_list[list_index ]
        
        
        folium.Polygon(locations=area,
        color=color_list[list_index],
        weight=2,
        fill=True,
        fill_opacity=0.1,
        opacity=0.8).add_to(lay_cluster)

###################################################################################

        #all of the above code is for the lines cornered for the clusters
        #below is for having different types of Maps in one file (interactive)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)
    #these lines are for making different types of maps and making your map interactive with clusters
    
####################################################################################
   
    return m

 

#%% Final Map visualization


m= create_map(hospitals,property)
m.save('Output/Karachi Hospitals Map.html')    