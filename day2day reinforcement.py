# -*- coding: utf-8 -*-
"""
Created on Tue May 30 13:42:26 2017

@author: Camden Ko camdenko@gmail.com
"""
from __future__ import division
import csv
import sys
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw()
filename = askopenfilename()
numIterations = int(raw_input("# of iterations: "))
endTime = int(raw_input("When does the experiment end (minutes)?"))
numDays = 12

probDist = []   # probability of sequetial opening for each trial simulated
experimentalProbDist = [] # actual numbers for sequential opening
dayProb = []   # probability for each day
ratProb = []  # probability for each rat
rawInput = []
openData = []

dataFile = open(filename, 'r')
dataReader = csv.reader(dataFile)
for row in dataReader:      # reads in data from chosen csv file
    rawInput.append(row),

# traverses list and converts the values to ints then converts it to
# 0 for non-opener or 1 for opener
for row_index, row in enumerate(rawInput):
    for col_index, item in enumerate(row):
        rawInput[row_index][col_index] = int(rawInput[row_index][col_index])
        if(rawInput[row_index][col_index] < endTime):
            rawInput[row_index][col_index] = 1.0
        else:
            rawInput[row_index][col_index] = 0.0
        
# totalOpeners is the total number of opens
totalOpeners = np.sum(rawInput)

inputArray = np.array(rawInput)
# calculate probability between days
dayProb = inputArray.sum(axis = 0)

# calculate probability between rats
ratProb = inputArray.sum(axis = 1)

for row_index, row in enumerate(ratProb):
    ratProb[row_index] = (ratProb[row_index]) / totalOpeners

for row_index, row in enumerate(dayProb):
    dayProb[row_index] = (dayProb[row_index]) / totalOpeners

# iterating
for iteration in range(0, numIterations):
    randArr = np.random.rand(len(ratProb), len(dayProb))
    numSequent = 0.0
    numOpens = 0.0
    for row_index, row in enumerate(randArr):
        for col_index, item in enumerate(row):
            if(randArr[row_index][col_index] >= dayProb[col_index] * ratProb[row_index] * totalOpeners):
                randArr[row_index][col_index] = 0
            else:
                randArr[row_index][col_index] = 1
    for row_index in range(0, len(ratProb) - 1):
        for col_index in range(0, len(dayProb)):
            if(randArr[row_index][col_index] == 1):
                numOpens += 1.0
                if(randArr[row_index+1][col_index] ==1):
                    numSequent += 1.0
    probDist.append(numSequent / numOpens)
averageProbDist = sum(probDist) / len(probDist)

# calculate the actual values
numSequent = 0.0
numOpens = 0.0
for x in range(0,len(ratProb)-1):
    for y in range(0,len(dayProb)):
        if(inputArray[x][y] == 1):
            numOpens += 1
            if(rawInput[x+1][y] == 1):
                numSequent += 1
actualProb = numSequent / numOpens

numDeviate = 0.0
for iteration in range(0,numIterations):
    if abs(probDist[iteration] - averageProbDist) >= abs(actualProb - averageProbDist):
        numDeviate += 1
print("p = ")
print(numDeviate/numIterations)