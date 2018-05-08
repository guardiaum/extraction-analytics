import sys
import csv
import pandas as pd


def sortDoc(arg):
    if len(arg) > 1:
        inputFile = sys.argv[1]

        outputFile = sys.argv[2]

        category = pd.read_csv(inputFile, sep=',', encoding="utf-8", index_col=False, names=["category", "count"])

        sorted = category.sort_values(by=["count"], ascending=False)

        sorted.to_csv(outputFile, encoding="utf-8", index=False)
    else:
        print "Missing parameters"


def csvFormat(args):
    finalcontent = []

    input = args[1]
    output = args[2]

    with open(input) as f:
        content = f.readlines()

        for line in content:
            elements = line.replace("\n", "").split(",")
            finalcontent.append(elements[len(elements) - 1])

    df = pd.DataFrame(finalcontent)
    df.to_csv(output, mode='w', index=False, header=False, encoding='utf-8')


# sortDoc(sys.argv)
csvFormat(sys.argv)
