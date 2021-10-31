import pandas as pd
import numpy as np


data = pd.read_csv("text.csv", index_col="Loan_ID")



print('\n\nBOOLEAN INDEXING\n\n',data.loc[(data["Gender"]=="Female") & (data["Education"]=="Not Graduate") &(data["Loan_Status"]=="Y"), ["Gender","Education","Loan_Status"]])



def num_missing(x):
  return sum(x.isnull())


print("\n\nMissing values per column:\n\n")
print(data.apply(num_missing, axis=0)) 

print("\n\nMissing values per row:\n\n")
print(data.apply(num_missing, axis=1).head())
