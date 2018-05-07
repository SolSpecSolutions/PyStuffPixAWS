# coding: utf-8

#Import Modules
import pandas as pd
import csv
import os

#Variables
#procFolder = raw_input("Enter Project Folder Path: ")
procFolder = "G:\ImageProcessing\TGS"

#Load .tgs files into an array
tgsFiles = os.listdir(procFolder)

#Create .csv file from .tgs in the same folder
for file in tgsFiles:
    #print file
    baseFilename = os.path.splitext(file)[0]
    inFile = pd.read_csv(procFolder + "/" + file, header=None)
    inFile[0] = inFile[0] + '.jpg'
    inFile.to_csv(procFolder + "/" + baseFilename + ".csv", sep=",", index=False, header=False)
