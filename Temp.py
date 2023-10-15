import csv

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Seconds', 'Temperature'])
        writer.writerows(data)

def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

# Initialize variables
data = []

# Get user inputs
print("Enter temperatures and time stamps. Type 'STOP' in all caps to finish.")
previous_timestamp = 0

while True:
    user_input = input(f"Enter temperature and time stamp (M:SS) (Previous time stamp: {previous_timestamp // 60}:{previous_timestamp % 60:02}): ")

    if user_input == "STOP":
        break

    temperature, timestamp = user_input.split(" ")
    temperature = float(temperature)
    current_timestamp = convert_time_to_seconds(timestamp)

    data.append([previous_timestamp, temperature])

    # Fill in the seconds in between
    for sec in range(previous_timestamp + 1, current_timestamp):
        data.append([sec, temperature])

    previous_timestamp = current_timestamp

# Save data to CSV
save_to_csv(data, 'temperature_data.csv')

print("CSV file 'temperature_data.csv' created successfully.")
