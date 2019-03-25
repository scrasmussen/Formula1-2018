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
  'surname':drivers2019['surname'],
  'racePoints':0,
  'racesRaced':0,
  'racesFinished':0,
  'score':0
  })

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

# calculate fastest lap
# driverName = points['driverId'] == row['driverId']
print(points)
points.loc[points['surname'] == 'Ricciardo', 'score']  += (4 * 5)
points.loc[points['surname'] == 'Bottas', 'score']     += (7 * 5)
points.loc[points['surname'] == 'Verstappen', 'score'] += (2 * 5)
points.loc[points['surname'] == 'Räikkönen', 'score']  += (1 * 5)
points.loc[points['surname'] == 'Vettel', 'score']     += (3 * 5)
points.loc[points['surname'] == 'Hamilton', 'score']   += (3 * 5)
points.loc[points['surname'] == 'Magnussen', 'score']  += (1 * 5)

print(points.loc[points['surname'] == 'Magnussen', 'score'])
sys.exit()
for index,row in results2018.iterrows():
  driverId = points['driverId'] == row['driverId']
  test = row['driverId']
  # print(driverId,"::",test)

  position = row.position

  # calculate starting grid points
  gridPoints = calcGridPoints(row.grid)
  # calculate position change points
  (racePoints, raceFinished) = calcPositionChangePoints(row.grid,row.position)
  # calculate finishing position points
  racePoints += row.points
  # calculate if finished ahead of teammate


  # print(row)
  score = racePoints + raceFinished + gridPoints

  points.loc[driverId,'racePoints'] += racePoints
  points.loc[driverId,'racesRaced'] += 1
  points.loc[driverId,'racesFinished'] += raceFinished
  points.loc[driverId,'score'] += score

  # == TODO ==
  # fastest lap
  # finish ahead of teammate


  # results2018 = results[ results["raceId"].isin(races2018) &
  #   results["driverId"].isin(drivers2019["driverId"])]
  # print(row['fastestLap'])
  # print(row)
  # if (row['fastestLap'].isin(points["driverId"])):
  #   print(row)

print(points)
print('Fin')



# printing
# print(races2018)
# print(drivers2019["driverID"])



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
