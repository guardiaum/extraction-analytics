import sys
import csv
import pandas as pd

if len(sys.argv) > 1:
	inputFile = sys.argv[1]

	outputFile = sys.argv[2]

	category = pd.read_csv(inputFile, sep=',', encoding="utf-8", index_col=False, names=["category", "count"])

	sorted = category.sort_values(by=["count"], ascending=False)

	sorted.to_csv(outputFile, encoding="utf-8", index=False);
else:
	print "Missing parameters"
