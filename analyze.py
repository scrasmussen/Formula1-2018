import numpy as np
import pandas as pd
import sys

def getSec(time):
  m, s = time.split(':')
  return (float(m)*60 + float(s))

def calcGridPoints(grid):
  if (grid > 10):
    return 0
  return 11 - grid

def calcPositionChangePoints(grid, position):
# return value (int:racePoints,bool:raceFinished)
  if (position == "\\N"):
    return (-15,0)
  finished = 1
  change = int(position) - int(grid)

  if (change > 0):
    if (change > 5):
      return (10, finished)
    else:
      return (change*2, finished)
  else: # change <= 0
    if (grid <= 10):
      change *= 2
      if (change < -10):
        return(-10,finished)
      return(change,finished)
    else: # grid > 10
      if (change < -5):
        return(-5,finished)
      return(change,finished)




# drivers
driverHeader = ["driverId", "driverRef", "number","code","forename","surname",
  "dob","nationality","url"]
drivers2019 = pd.read_csv('data/driver_2019.csv', names=driverHeader)
# races
racesHeader = ["raceId","year","round","circuitId","name","date","time","url"]
races = pd.read_csv('data/races.csv', names=racesHeader)
races2018=races.query("year=='2018'")['raceId']
# race results
resultsHeader = ["resultId","raceId","driverId","constructorId","number","grid",
  "position","positionText","positionOrder","points","laps","time",
  "milliseconds","fastestLap","rank","fastestLapTime","fastestLapSpeed",
  "statusId"]
results = pd.read_csv('data/results.csv', names=resultsHeader)
# qualifying results
qualifyingHeader = ["qualifyId","raceId","driverId","constructorId","number",
  "position","q1","q2","q3"]
qualifying = pd.read_csv('data/qualifying.csv', names=qualifyingHeader)

# filter results and qualifying
results2018 = results[ results["raceId"].isin(races2018) &
  results["driverId"].isin(drivers2019["driverId"])]
qualifying2018 = qualifying[ qualifying["raceId"].isin(races2018) &
  qualifying["driverId"].isin(drivers2019["driverId"])]

# setup dataframes
points = pd.DataFrame({
  'driverId':drivers2019['driverId'],
  'driverId':drivers2019['driverId'],
  'surname':drivers2019['surname'],
  'racePoints':0,
  'racesRaced':0,
  'racesFinished':0,
  'score':0,
  'team_score':0,
  'cost':0.,
  'worth_score':0.,
  'worth_team_score':0.
  })

con = results2018.constructorId.unique()

rl = results2018.raceId.unique()
raceList = pd.DataFrame({
  'raceList':rl,
  'fastestDriver':-1,
  'fastestLapTime':999.0})


for index,row in qualifying2018.iterrows():
  driverId = points['driverId'] == row['driverId']
  score = 0
  if (row.q1 == "\\N"):
    score = -5
  elif (row.q2 == "\\N"):
    score = 1
  elif (row.q3 == "\\N"):
    score = 2
  else:
    score = 3
  points.loc[driverId,'score'] += score
  if (score != -5):
      points.loc[driverId,'team_score'] += score

# calculate fastest lap
points.loc[points['surname'] == 'Ricciardo', 'score']  += (4 * 5)
points.loc[points['surname'] == 'Bottas', 'score']     += (7 * 5)
points.loc[points['surname'] == 'Verstappen', 'score'] += (2 * 5)
points.loc[points['surname'] == 'Räikkönen', 'score']  += (1 * 5)
points.loc[points['surname'] == 'Vettel', 'score']     += (3 * 5)
points.loc[points['surname'] == 'Hamilton', 'score']   += (3 * 5)
points.loc[points['surname'] == 'Magnussen', 'score']  += (1 * 5)

for index,row in results2018.iterrows():
  driverId = points['driverId'] == row['driverId']
  test = row['driverId']

  # calculate starting grid points
  gridPoints = calcGridPoints(row.grid)
  # calculate position change points
  (racePoints, raceFinished) = calcPositionChangePoints(row.grid,row.position)
  if (racePoints == -15):
    teamPoints = 0
  else:
    teamPoints = racePoints
  # calculate finishing position points
  racePoints += row.points
  teamPoints += row.points
  # calculate if finished ahead of teammate


  # print(row)
  score = racePoints + raceFinished + gridPoints
  team_score = teamPoints + gridPoints

  points.loc[driverId,'racePoints'] += racePoints
  points.loc[driverId,'racesRaced'] += 1
  points.loc[driverId,'racesFinished'] += raceFinished
  points.loc[driverId,'score'] += score
  points.loc[driverId,'team_score'] += team_score

  # == TODO ==
  # fastest lap
  # finish ahead of teammate


  # results2018 = results[ results["raceId"].isin(races2018) &
  #   results["driverId"].isin(drivers2019["driverId"])]
  # print(row['fastestLap'])
  # print(row)
  # if (row['fastestLap'].isin(points["driverId"])):
  #   print(row)


# adding cost and average points per dollar
points.loc[points['surname'] == 'Hamilton', 'cost']   += 30.5
points.loc[points['surname'] == 'Vettel', 'cost']     += 27.5
points.loc[points['surname'] == 'Verstappen', 'cost'] += 24.5
points.loc[points['surname'] == 'Leclerc', 'cost']    += 23.5
points.loc[points['surname'] == 'Bottas', 'cost']     += 20.5
points.loc[points['surname'] == 'Gasly', 'cost']      += 17.5
points.loc[points['surname'] == 'Ricciardo', 'cost']  += 12.0
points.loc[points['surname'] == 'Hülkenberg', 'cost'] += 11.8
points.loc[points['surname'] == 'Pérez', 'cost']      += 11.0
points.loc[points['surname'] == 'Magnussen', 'cost']  += 10.0
points.loc[points['surname'] == 'Räikkönen', 'cost']  += 10.0
points.loc[points['surname'] == 'Grosjean', 'cost']   += 9.3
points.loc[points['surname'] == 'Sainz', 'cost']      += 7.7
points.loc[points['surname'] == 'Stroll', 'cost']     += 7.4
points.loc[points['surname'] == 'Norris', 'cost']     += 6.9
points.loc[points['surname'] == 'Giovinazzi', 'cost'] += 6.8
points.loc[points['surname'] == 'Albon', 'cost']      += 6.0
points.loc[points['surname'] == 'Russell', 'cost']    += 6.0
points.loc[points['surname'] == 'Kubica', 'cost']     += 5.5
points.loc[points['surname'] == 'Kvyat', 'cost']      += 5.5


# Hamilton
# Bottas
# Verstappen
# Vettel
# Leclerc
# Magnussen
# Hülkenberg
# Räikkönen
# Stroll
# Kvyat
# Gasly
# Pérez
# Albon
# Giovinazzi
# Russell
# Norris
# Kubica
# Grosjean
# Ricciardo
# Sainz



 # points.score.div(points.cost, axis='columns')
points.worth_score = points.score.div(points.cost)
points.worth_team_score = points.team_score.div(points.cost)

# z = zip(points.surname, points.worth_score)
z = zip(points.surname, points.score)
print(points)
for i in z:
  print(i)
print('Fin')



  # calculate fastest lap
  # print(raceList[raceList.raceList==row.raceId].fastestLapTime)
  # print(raceList.loc[raceList.raceList==row.raceId,'fastestLapTime'])
  # fastestLap =  raceList[raceList.raceList==row.raceId].fastestLapTime
  # rowLapTime = getSec(row.fastestLapTime)
  # print("====")
  # print(fastestLap, "|||", rowLapTime)
  # if (fastestLap > rowLapTime):
  #   raceList.loc[raceList.raceList==row.raceId, 'fastestLapTime'] = rowLapTime
  #   raceList.loc[raceList.raceList==row.raceId, 'fastestDriver'] = row.driverId
  #   # print(raceList.loc[raceList.raceList==row.raceId, 'fastestLapTime'])
  #   # print(raceList)
  #   # sys.exit()
  #   # print(raceList)
  # # print("row.time = ", row.time)
