import numpy as np
import pandas as pd
import itertools as it
import sys
import time

budget = 100 # 100
week=0 # current week
starting_week = 0

# gone but not forgotten
# 0,"Magnussen",8
# 0,"Grosjean",5.9
# 0,"Kvyat",9.8
# 0,"Albon",20.6




isDriver = 1
isConstructor = 0
pp="{0:0.02f}"
pd.options.display.float_format = pp.format
def pprint(current_group, total_cost, total_points, turbo):
  b = [pp.format(i) for i in [total_cost, total_points]]
  print("\ncost: "+str(b[0]) + " points: " + str(b[1]) + " turbo: " + turbo)
  print(current_group)

#
# Start Importing Data
#

# import race data
fantasy2022 = ['Week','Year','Name','Points','isDriver','GridPosition',
               'FinalResult']
f = pd.read_csv('data/2022_fantasy_points.csv', names=fantasy2022,
                 dtype={'isDriver':bool})

# limit weeks
ending_week =  max(f.Week) #  ----PRESEASON GUESSING----
lf = f[f.Week == ending_week]

# lf.Points -= f[f.Week == starting_week].Points
# sys.exit()

lf.drop(['Year','Week'], axis=1, inplace=True)

driver_names_subset = ['Name', 'Points', 'GridPosition','FinalResult']
driver_data      = lf.loc[lf.isDriver == isDriver, driver_names_subset]
constructor_data = lf.loc[lf.isDriver == isConstructor, ['Name', 'Points']]
# print("Range: week " + str(starting_week) + " to week " +  str(ending_week))

# fix types, need to do this here because None's aren't numbers
driver_data.GridPosition = pd.to_numeric(driver_data.GridPosition)
driver_data.FinalResult = pd.to_numeric(driver_data.FinalResult)

# import cost data
cost_names = ["Week","Name","Cost"]
cost_data = pd.read_csv('data/2022_cost.csv', names=cost_names)
current_week = cost_data[cost_data.Week == week]
cost  = current_week[["Name","Cost"]]


# get averages
week_div = (ending_week-starting_week+1)
driver_data['AveragePoints'] = driver_data.Points / week_div
constructor_data['AveragePoints'] = constructor_data.Points / week_div


# merge points data with costs
drivers = pd.merge(cost,driver_data,on='Name',how='right',)
teams   = pd.merge(cost,constructor_data,on='Name',how='right')

# find average point per million
drivers['Points/Mil'] = drivers.Points / drivers.Cost
teams['Points/Mil']   = teams.Points / teams.Cost

# sort data
drivers = drivers.sort_values('Points/Mil',ascending=False)
teams   = teams.sort_values('Points/Mil',ascending=False)
# drivers = drivers.sort_values('Points',ascending=False)
# teams   = teams.sort_values('Points',ascending=True)

print(teams)
print()
print(drivers)
# sys.exit()
#
# Iterate to find best point combination of team and drivers
#

iterDrivers = list(it.combinations(drivers.Name, 5))
best_points = 0
best_team   = ''

# converted teams to zipped list for quicker access
team_list = list(zip(teams.Name, teams.Points, teams.Cost))
name_i=0
points_i=1
cost_i=2

# only look at Mercedes cause they are destroying, speeds up algorithm
team_mercedes = list((t for t in team_list
                      if(t[name_i] == 'Red Bull')))
                      # if(t[name_i] == 'Mercedes')))
                      # if(t[name_i] == 'Mercedes' or t[name_i] == 'Red Bull')))

# print(team_list)
# sys.exit()

# begin iteration
start = time.time()
for driverList in iterDrivers:
  # for team in team_list:
  for team in team_mercedes:

    # required = ('Hamilton', 'Russell', 'Perez', 'Stroll')
    # required = ('Russell', 'Perez')
    # required = ('Schumacher')
    # if not set(required).issubset(driverList):
    #   break

    team_cost   = team[cost_i]
    driver_cost   = drivers.loc[drivers['Name'].isin(driverList)].Cost.sum()
    total_cost   = team_cost + driver_cost
    if (total_cost > budget):
      break

    team_points = team[points_i]
    driver_points = drivers.loc[drivers['Name'].isin(driverList)].Points.sum()
    turbo = drivers.loc[drivers.Name.isin(driverList) & (drivers.Cost <= 20)]
    turbo_points = turbo.Points.max()
    turbo_driver = turbo[turbo.Points == turbo_points].Name
    total_points = team_points + driver_points + turbo_points

    best_drivers = []

    if (total_points >= best_points):
      best_points  = total_points
      best_cost    = total_cost
      best_team    = team[name_i]
      best_drivers = driverList
      best_turbo   = turbo_driver.iloc[0]
      current_group    = best_team + ", " + ", ".join(driverList)
      pprint(current_group, total_cost, total_points, best_turbo)
    elif (total_points >= best_points - 25): # 200):
    # elif (total_points >= 2600): # 200):
      current_group = team[name_i] + ", " + ", ".join(driverList)
      pprint(current_group, total_cost, total_points, best_turbo)
end = time.time()
# zip list with only Mercedes taking 46.7 seconds, 48.58, 45.77

# print results
print("\n---Finished Analysis---")
print("Runtime: " + pp.format(end-start) + " seconds")
print("Best team: " + best_team)
print("Best drivers: " + ", ".join(best_drivers))
print("Best turbo: "   + best_turbo)
print("Best points: "  + pp.format(best_points))
print("Total cost: "   + pp.format(best_cost))
print("\nFIN")
