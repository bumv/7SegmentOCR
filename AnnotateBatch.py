import os
import shutil

# Define paths
source_folder = "Amp"
output_folder = "AmpFramesAnnotate"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get a list of all the files in the source folder
files = os.listdir(source_folder)

# Iterate over every 500th image
for i, file in enumerate(files):
    if i % 20 == 0:  # Check if it's every 500th image
        source_path = os.path.join(source_folder, file)
        output_path = os.path.join(output_folder, file)
        shutil.copy2(source_path, output_path)