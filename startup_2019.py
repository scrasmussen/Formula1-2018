import numpy as np
import pandas as pd
import itertools as it
import sys



# races
fantasy2019 = ["Week","Name","Points","isDriver"]
f = pd.read_csv('data/fantasy2019.csv', names=fantasy2019)
# f = f.drop("Team/Driver",1)
mean = f.groupby(['Week','Name']).mean()
ave_points = mean.sort_values('Points',ascending=False)

cost_names = ["Week","Name","Cost"]
c1 = pd.read_csv('data/fantasy2019_cost.csv', names=cost_names)
cost  = c1[["Name","Cost"]]
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

iterDrivers = list(it.combinations(drivers.Name, 5))
best_points = 0
best_team   = ''
for driverList in iterDrivers:
  for team in teams.Name:
    team_cost   = teams.loc[teams['Name']==team].Cost.item()
    driver_cost   = drivers.loc[drivers['Name'].isin(driverList)].Cost.sum()
    total_cost   = team_cost + driver_cost
    if (total_cost > 100.3):
      break

    team_points = teams.loc[teams['Name']==team].Points.item()
    driver_points = drivers.loc[drivers['Name'].isin(driverList)].Points.sum()
    total_points = team_points + driver_points
    if (total_points == best_points):
      print("REPEAT? @ ",total_points, " and ", total_cost)
    if (total_points > best_points):
      best_points  = total_points
      best_cost    = total_cost
      best_team    = team
      best_drivers = driverList
      print(total_cost, total_points)


print("---Finished Analysis---")
print("Best team ", best_team)
print("Best drivers", best_drivers)
print("Best points", best_points)
print("Total cost = ", str(total_cost))
print("\nFIN")
