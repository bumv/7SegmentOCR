import pandas as pd

# Load the CSV file
results = pd.read_csv('Results.csv')

# Add a new column 'power' by multiplying 'amps' and 'volts'
results['Power'] = results['Amps'] * results['Volts']

# Save the updated DataFrame to a new CSV file
results.to_csv('updated_results.csv', index=False)