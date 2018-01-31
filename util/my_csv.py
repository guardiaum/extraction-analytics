import csv
import glob
import os
import numpy as np
import itertools

# gets all csv files under csv directory
def readCSVDirectory(dir):
	os.chdir(dir)
	return glob.glob("*.csv")

# read csv file
def readCSVFile(file):
	with open(file, 'r') as f:
		category = list(csv.reader(f, delimiter=","))
		category = np.array(category)
		return category
