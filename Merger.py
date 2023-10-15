import pandas as pd

# Load the CSV files
amps_df = pd.read_csv('AmpsPerSecond.csv')
volts_df = pd.read_csv('VoltsPerSecond.csv')
temp_df = pd.read_csv('TemperaturePerSecond.csv')

# Merge the data frames on the 'seconds' column
merged_df = pd.merge(amps_df, volts_df, on='Seconds')
merged_df = pd.merge(merged_df, temp_df, on='Seconds')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('Results.csv', index=False)
