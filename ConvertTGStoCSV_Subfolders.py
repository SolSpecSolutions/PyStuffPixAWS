# coding: utf-8

#Import Modules
import pandas as pd
import csv
import os

#Variables
pFolder = "G:\ImageProcessing\TGS"

#Load subfolders into an array
tgsFolders = os.listdir(pFolder)

#Loop through subfolders and create .csv file from .tgs in the subfolder
for folder in tgsFolders:
    file = pFolder + "\\" + folder + "\\" + folder + ".tgs"
    baseFilename = os.path.splitext(file)[0]
    inFile = pd.read_csv(file, header=None)
    inFile[0] = inFile[0] + '.jpg'
    inFile.to_csv(baseFilename + ".csv", sep=",", index=False, header=False)
