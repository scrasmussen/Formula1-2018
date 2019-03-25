import numpy as np
import pandas as pd

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
# print(results["raceId"])
# print(races2018['raceId'])

print(results[ results["raceId"].isin(races2018) &
  results["driverId"].isin(drivers2019["driverId"])])
# print(results[ results["driverId"].isin(drivers2019["driverId"]) ])
# print(drivers2019["driverId"])


# printing
# print(races2018)
# print(drivers2019["driverID"])
