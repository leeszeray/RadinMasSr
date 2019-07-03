import pandas as pd

data = pd.read_excel("OutputFile.xlsx")
# print(data)
#
# print(pd.get_option("display.max_rows"))
#
# print(pd.get_option("display.max_columns"))

df = pd.DataFrame(data)

df_revised = df.transpose()

df_revised.to_csv("OutputFile2.csv")
