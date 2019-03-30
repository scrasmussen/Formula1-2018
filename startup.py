import numpy as np
import pandas as pd
import sys

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


# calculate fastest lap
# points.loc[points['surname'] == 'Ricciardo', 'score']  += (4 * 5)
# points.loc[points['surname'] == 'Bottas', 'score']     += (7 * 5)
# points.loc[points['surname'] == 'Verstappen', 'score'] += (2 * 5)
# points.loc[points['surname'] == 'Vettel', 'score']     += (3 * 5)
# points.loc[points['surname'] == 'Hamilton', 'score']   += (3 * 5)
# points.loc[points['surname'] == 'Magnussen', 'score']  += (1 * 5)


# Hamilton
# Bottas
# Verstappen
# Vettel
# Leclerc
# Magnussen
# Hulkenberg
# Raikkonen
# Stroll
# Kvyat
# Gasly
# Perez
# Albon
# Giovinazzi
# Russell
# Norris
# Kubica
# Grosjean
# Ricciardo
# Sainz
