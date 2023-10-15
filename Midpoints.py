import pandas as pd

# Load the CSV data into a DataFrame
df = pd.read_csv('Results.csv')

# Group the data by Temperature and find the midpoint
midpoints = df.groupby('Temperature')['Seconds'].mean()

# Print the results
templist=[]
secondslist=[]

for seconds in midpoints.items():
    secondslist.append(seconds)

for k in secondslist:
    print (k[1])