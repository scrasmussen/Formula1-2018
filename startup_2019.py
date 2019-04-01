import numpy as np
import pandas as pd
import sys

# races
fantasy2019 = ["Week","Name","Points","Team/Driver"]
f = pd.read_csv('data/fantasy2019.csv', names=fantasy2019)
f = f.drop("Team/Driver",1)
mean = f.groupby(['Week','Name']).mean()
ave_points = mean.sort_values('Points',ascending=False)

cost_names = ["Week","Name","Cost"]
c1 = pd.read_csv('data/fantasy2019_cost.csv', names=cost_names)
cost  = c1[["Name","Cost"]]
cost = pd.merge(cost,ave_points,on='Name',how='outer')
p = cost.sort_values('Points',ascending=False)

div = (p.Points / p.Cost).T
div = pd.DataFrame(div, columns=["Average"])

p = p.join(div,how="outer")
a = p.sort_values('Average',ascending=False)
