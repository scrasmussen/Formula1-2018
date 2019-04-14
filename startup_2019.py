import numpy as np
import pandas as pd
import itertools as it
import sys
import time



# races
fantasy2019 = ["Week","Name","Points","isDriver"]
f = pd.read_csv('data/fantasy2019.csv', names=fantasy2019)
# f = f.drop("Team/Driver",1)
# f = f[f.Name != "Mercedes"]
# print(f)
mean = f.groupby(['Week','Name']).mean()
ave_points = mean.sort_values('Points',ascending=False)

cost_names = ["Week","Name","Cost"]
c1 = pd.read_csv('data/fantasy2019_cost.csv', names=cost_names)
week3 = c1[c1.Week == 3]
cost  = week3[["Name","Cost"]]
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
name_i=0
points_i=1
cost_i=2
team_list = list(zip(teams.Name, teams.Points, teams.Cost))
# only look at Mercedes cause they are destroying, speeds up algorithm
team_mercedes = list((t for t in team_list if t[name_i] == 'Mercedes'))

# sys.exit()
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

    if (total_points == best_points):
      print("REPEAT! ",total_points, " and ", total_cost)
    if (total_points >= best_points):
      best_points  = total_points
      best_cost    = total_cost
      best_team    = team[name_i]
      best_drivers = driverList
      best_turbo   = turbo_driver
      best_list    = best_team + ", " + ", ".join(driverList)
      b = ["{0:0.2f}".format(i) for i in [total_cost, total_points]]
      print("\ncost: "+str(b[0]) + " points: " + str(b[1]) + " turbo: " + best_turbo.item())
      print(best_list)
    elif (total_points >= 200): # best_points - 2):
      choices    = team[name_i] + ", " + ", ".join(driverList)
      b = ["{0:0.2f}".format(i) for i in [total_cost, total_points]]
      print("\ncost: "+str(b[0]) + " points: " + str(b[1]) + " turbo: " + best_turbo.item())
      print(choices)
end = time.time()
# zip list with only Mercedes taking 46.7 seconds

print("\n---Finished Analysis---")
print("Took ",end-start," seconds")
print("Best team: " + best_team)
print("Best drivers: " + ", ".join(best_drivers))
print("Best points: "  + "{0:0.02f}".format(best_points))
print("Total cost: "   + "{0:0.02f}".format(best_cost))
print("\nFIN")
