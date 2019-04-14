import numpy as np
import pandas as pd
import itertools as it
import sys
import time

def pprint(current_group, total_cost, total_points, turbo):
  b = ["{0:0.2f}".format(i) for i in [total_cost, total_points]]
  print("\ncost: "+str(b[0]) + " points: " + str(b[1]) + " turbo: " + turbo)
  print(current_group)

# import race data
fantasy2019 = ["Week","Year","Name","Points","isDriver"]
f = pd.read_csv('data/fantasy2019.csv', names=fantasy2019)
f.drop(['Year','Week'], axis=1, inplace=True)
# lr = f.drop(['Week','isDriver'], axis=1)
mean = f.groupby(['Name']).mean()
ave_points = mean.sort_values('Points',ascending=False)

# import cost data
cost_names = ["Week","Name","Cost"]
cost_data = pd.read_csv('data/fantasy2019_cost.csv', names=cost_names)
current_week = cost_data[cost_data.Week == 3]
cost  = current_week[["Name","Cost"]]
cost = pd.merge(cost,ave_points,on='Name',how='outer')
p = cost.sort_values('Points',ascending=False)

ave_Label='Points/Cost'
div = (p.Points / p.Cost).T
div = pd.DataFrame(div, columns=[ave_Label])

p = p.join(div,how="outer")
a = p.sort_values(ave_Label,ascending=False)
print("p: list sorted by points")
print("a: list sorted by points/cost")

drivers = p.query("isDriver == True")
teams   = p.query("isDriver == False")
print(teams)
print(drivers)
# sys.exit()

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

# zip list with only Mercedes taking 46.7 seconds, 48.58, 45.77
end = time.time()
pp="{0:0.02f}"

print("\n---Finished Analysis---")
print("Runtime: " + pp.format(end-start) + " seconds")
print("Best team: " + best_team)
print("Best drivers: " + ", ".join(best_drivers))
print("Best points: "  + pp.format(best_points))
print("Total cost: "   + pp.format(best_cost))
print("\nFIN")
