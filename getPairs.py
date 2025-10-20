import math
import copy
import numpy as np

from simulator import runSim
from teCosts import getTeCosts

teCosts = getTeCosts()

L = 168
x0 = 9.1375e19
k = 5.601e-20    

def getMax(x):
    hr = L / (1 + np.exp(-k * (x - x0)))
    return hr * 3600

a_multi = 85041
cube = 60

simTimes = {}
simFarms = {}

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
            maxTime = list(range(max / 168, max, max / 168))

            simTime, simFarm = runSim(rounds, maxTime, a_multi, cube, endCost, start)
            simTime = f"{simTime // 86400} days, {(simTime%86400)//3600} hours and {(simTime%3600)//60} minutes."

            file.write(f"Pair: {start} TE to {end} TE. This took {simTime}")
            simTimes[f"{start}-{end}"] = simTime
