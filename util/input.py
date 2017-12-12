import os

# Selects a group of files
def readGroupOfFiles(datasets_path):
	
	# Read input
	input_files = os.listdir(datasets_path)
	
	files = []
	for f in input_files:
		if f.endswith(".csv"):
			files.append(f)
	
	for index, f in enumerate(files):
		print("%s - %s" % (index, f))
	
	
	# Datasets quantity
	datasetsNumber = int(input("Inform datasets quantity: "))
	
	# Get files
	options = []
	for index in range(0, datasetsNumber):
		op = int(input("Inform dataset index: "))
		options.append(op)
	
	# Vector of selected categories
	categoriesName = []
	for option in options:
		categoriesName.append(files[option])
	
	# Name for outputfile
	outputFileName = str(input("Name for output file: ")) # Inform name for output file
	
	title = str(input("Inform title for plot if needed: "))
	
	subtitle = str(input("Inform subtitle for plot if needed: "))
	return categoriesName, outputFileName, title, subtitle
	
# Selects a group of files
def readFile(datasets_path):
	# Read input
	input_files = os.listdir(datasets_path)
	
	files = []
	for f in input_files:
		if f.endswith(".csv"):
			files.append(f)
	
	for index, f in enumerate(files):
		print("%s - %s" % (index, f))
	
	# Get file
	op = input("Choose one dataset (index): ")
	
	# selected file
	categoryName = files[op]
	
	return categoryName
