import my_csv
import pandas as pd

files = my_csv.readCSVDirectory("/home/johny/workspace/extraction-analytics/datasets/templates")
output_path = "/home/johny/workspace/extraction-analytics/results/csv/templates/count-templates-size.csv"
output = []

for file in files:
    with open(file) as f:
        content = f.readlines()

        for line in content:
            elements = line.replace("\n", "").split(",")
            template_name = elements[0]
            properties_count = len(elements) - 1

            output.append([template_name, properties_count])

df = pd.DataFrame(output)
df.to_csv(output_path, mode='w', index=False, header=False, encoding='utf-8')