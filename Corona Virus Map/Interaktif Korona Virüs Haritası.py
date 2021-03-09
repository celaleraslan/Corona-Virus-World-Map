import pandas
import openpyxl
import folium

data = pandas.read_excel("world_coronavirus_cases.xlsx")

latitudes = list(data["Latitude"])
longitudes = list(data["Longitude"])
total_case = list(data["Total Case"])
deaths = list(data["Deaths"])
actives = list(data["Active Cases"])
population = list(data["Population"])
total_test = list(data["Total Test"])

case_number_map = folium.FeatureGroup(name="Total Number of Cases Map")
""" Allows us to name the layer we created."""
death_rate_map = folium.FeatureGroup(name="Mortality Map")
active_case_map = folium.FeatureGroup(name="Active Case Map")
test_rate_map = folium.FeatureGroup(name="Test Rate Map")
population_distribution_map=folium.FeatureGroup(name="Population Distribution Map")

def number_of_cases_color(case):
    if(case<100000):
        return "green"
    elif(case < 300000):
        return "white"
    elif(case <750000):
        return "orange"
    else:
        return "red"

def number_of_cases_radius(case):
    if (case < 100000):
        return 20000
    elif (case < 300000):
        return 60000
    elif (case < 750000):
        return 100000
    else:
        return 200000

def death_rate_radius(case, death):
    if ((death/case)*100 < 2.5):
        return 20000
    elif ((death/case)*100 < 5):
        return 60000
    elif ((death/case)*100 < 7.5):
        return 100000
    else:
        return 200000

def mortality_color(case, death):
    if ((death/case)*100 < 2.5):
        return "green"
    elif ((death/case)*100 < 5):
        return "white"
    elif ((death/case)*100 < 7.5):
        return "orange"
    else:
        return "red"

def active_case_color(active):
    if (active < 100000):
        return "green"
    elif (active < 300000):
        return "white"
    elif (active < 750000):
        return "orange"
    else:
        return "red"

def active_case_radius(active):
    if (active < 100000):
        return 20000
    elif (active < 300000):
        return 60000
    elif (active < 750000):
        return 100000
    else:
        return 200000

def test_rate_radius(population, test):
    if ((test / population) * 100 < 2.5):
        return 200000
    elif ((test / population) * 100 < 5):
        return 100000
    elif ((test / population) * 100 < 7.5):
        return 60000
    else:
        return 30000

def test_rate_color(population, test):
    if ((test / population) * 100 < 2.5):
        return "red"
    elif ((test / population) * 100 < 5):
        return "orange"
    elif ((test / population) * 100 < 7.5):
        return "white"
    else:
        return "green"

world_map = folium.Map(tiles="Cartodb dark_matter")

for latitude,longitude,number_of_cases in zip(latitudes,longitudes,total_case):
    case_number_map.add_child(folium.Circle(location=(latitude,longitude),
                                radius=vaka_sayisi_radius(number_of_cases),
                        color=number_of_cases_color(number_of_cases_color),
                                      fill_color="blue",fill_opacity=0.3))

for latitude, longitude, number_of_cases, death in zip(latitudes, longitudes, total_case, deaths):
    death_rate_map.add_child(folium.Circle(location=(latitude,longitude),
                                      radius=death_rate_radius(number_of_cases,death),
                                      color=mortality_color(number_of_cases,death),
                fill_color=mortality_color(number_of_cases,death),fill_opacity=0.3))

for latitude, longitude, active in zip(latitudes, longitudes, actives):
    active_case_map.add_child(folium.Circle(location=(latitude,longitude),
                                      radius=active_case_radius(active),
                                      color=active_case_color(active),
                            fill_color=active_case_color(active),fill_opacity=0.3))

for latitude, longitude, country_population, test in zip(enlemler, boylamlar, population, total_test):
    test_rate_map.add_child(folium.Circle(location=(latitude, longitude),
                                    radius=test_rate_radius(country_population,test),
                                    color=test_rate_color(country_population,test),
                                fill_color=test_rate_color(country_population,test), fill_opacity=0.3))

population_distribution_map.add_child(folium.GeoJson(data=(open("world.json","r",encoding="utf-8-sig").read()),
                                                      style_function = lambda x:{'fillColor':'green'
                                                      if(x["properties"]["POP2005"] < 20000000) else
                                                      'white' if(20000000 <= x["properties"]["POP2005"] <= 50000000) else
                                                      'orange' if(50000000 <= x["properties"]["POP2005"] <= 100000000) else 'red'}))

""" We opened our json file with GeoJson and we can change its color with style_function."""
world_map.add_child(case_number_map)
world_map.add_child(death_rate_map)
world_map.add_child(active_case_map)
world_map.add_child(test_rate_map)
world_map.add_child(population_distribution_map)

world_map.add_child(folium.LayerControl())
"""Allows to create layers in our map"""

world_map.save("world_map.html")
