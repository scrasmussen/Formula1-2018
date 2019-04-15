import numpy as np
import pandas as pd
import itertools as it
import sys
import time

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
fantasy2019 = ['Week','Year','Name','Points','isDriver','StartPosition',
               'PositionChange']
f = pd.read_csv('data/fantasy2019.csv', names=fantasy2019,
                 dtype={'isDriver':bool})
f.drop(['Year','Week'], axis=1, inplace=True)
# lr = f.drop(['Week','isDriver'], axis=1)
driver_names_subset = ['Name', 'Points', 'StartPosition','PositionChange']
driver_data      = f.loc[f.isDriver == isDriver, driver_names_subset]
constructor_data = f.loc[f.isDriver == isConstructor, ['Name', 'Points']]

# fix types, need to do this here because None's aren't numbers
driver_data.StartPosition = pd.to_numeric(driver_data.StartPosition)
driver_data.PositionChange = pd.to_numeric(driver_data.PositionChange)

# import cost data
cost_names = ["Week","Name","Cost"]
cost_data = pd.read_csv('data/fantasy2019_cost.csv', names=cost_names)
current_week = cost_data[cost_data.Week == 3]
cost  = current_week[["Name","Cost"]]

# get averages
driver_ave       = driver_data.groupby(['Name']).mean()
constructor_ave  = constructor_data.groupby(['Name']).mean()

# merge points data with costs
drivers = pd.merge(cost,driver_ave,on='Name',how='right',)
teams   = pd.merge(cost,constructor_ave,on='Name',how='right')

# find average point per million
ave_Label='Points/Cost'
driver_div = pd.DataFrame((drivers.Points / drivers.Cost).T,columns=[ave_Label])
teams_div  = pd.DataFrame((teams.Points  /  teams.Cost).T, columns=[ave_Label])
drivers = drivers.join(driver_div,how="outer")
drivers = drivers[['Name', 'Cost', 'Points', 'Points/Cost', 'StartPosition',
                   'PositionChange']]
teams   = teams.join(teams_div,how="outer")

# sort data
drivers = drivers.sort_values('Points',ascending=False)
teams   = teams.sort_values('Points',ascending=False)

print(teams)
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
team_mercedes = list((t for t in team_list if t[name_i] == 'Mercedes'))

# begin iteration
start = time.time()
for driverList in iterDrivers:
  for team in team_mercedes:
    team_cost   = team[cost_i]
    driver_cost   = drivers.loc[drivers['Name'].isin(driverList)].Cost.sum()
    total_cost   = team_cost + driver_cost
    if (total_cost > 101.2):
      break
    team_points = team[points_i]
    driver_points = drivers.loc[drivers['Name'].isin(driverList)].Points.sum()
    turbo = drivers.loc[drivers.Name.isin(driverList) & (drivers.Cost <= 19)]
    turbo_points = turbo.Points.max()
    turbo_driver = turbo[turbo.Points == turbo_points].Name
    total_points = team_points + driver_points + turbo_points

    if (total_points >= best_points):
      best_points  = total_points
      best_cost    = total_cost
      best_team    = team[name_i]
      best_drivers = driverList
      best_turbo   = turbo_driver
      current_group    = best_team + ", " + ", ".join(driverList)
      pprint(current_group, total_cost, total_points, best_turbo.item())
    elif (total_points >= 200): # best_points - 2):
      current_group = team[name_i] + ", " + ", ".join(driverList)
      pprint(current_group, total_cost, total_points, best_turbo.item())
end = time.time()
# zip list with only Mercedes taking 46.7 seconds, 48.58, 45.77

# print results
print("\n---Finished Analysis---")
print("Runtime: " + pp.format(end-start) + " seconds")
print("Best team: " + best_team)
print("Best drivers: " + ", ".join(best_drivers))
print("Best points: "  + pp.format(best_points))
print("Total cost: "   + pp.format(best_cost))
print("\nFIN")
