import math
import copy
import numpy as np

from autoSim import runSim
from teCosts import getTeCosts

teCosts = getTeCosts()

def getMax(x):
    L = 168       # hours maximum
    x0 = 1e16     # midpoint of the curve (10 quadrillion)
    k  = 2.5e-16  # slope: controls how fast you approach L
    hr = L / (1 + np.exp(-k * (x - x0)))
    return hr * 3600  # convert hours → seconds

a_multi = 85041
cube = 60

simTimes = {}
simFarms = {}

# for test in [5e7, 1e10, 1e13, 1e15, 1e16, 1e17, 1e18, 1e19]:
#     print(f"{test:.1e} -> {getMax(test)/3600:.1f} hours")

def runPairs(file):
    global simTimes, simFarms
    for start in range(0, 59):
        for end in range(2, 61):
            if (end - start) < 2:
                continue

            startCost = 0
            if start > 0:
                startCost = teCosts[start-1]
            
            endCost = teCosts[end-1] - startCost

            start *= 5
            startCost *= 5
            end *= 5
            endCost *= 5

            rounds = list(range(3,4,1))

            max = getMax(endCost)
            maxTime = list(range(math.floor(max / 168), math.floor(max), math.floor(max / 168)))

            simTime, simFarm = runSim(rounds, maxTime, a_multi, cube, endCost, start)
            simTimeN = f"{simTime // 86400} days, {(simTime%86400)//3600} hours and {(simTime%3600)//60} minutes."

            start = int(start / 5)
            end = int(end / 5)

            file.write(f"Pair: {start} TE to {end} TE. This took {simTimeN} \n")
            simTimes[f"{start}-{end}"] = simTime
            simFarms[f"{start}-{end}"] = simFarm
        print(f"{start}/58")

with open("pairs_out.txt", "w") as file:
    runPairs(file)
