from roboflow import Roboflow
from PIL import Image
import os

# Initialize Roboflow
rf = Roboflow(api_key="APIKEY")
project = rf.workspace().project("more-mmd")
model = project.version(1).model

def get_bounding_box(image_path):
    response = model.predict(image_path, confidence=20).json()
    prediction = response["predictions"][0]
    x, y, width, height = prediction["x"], prediction["y"], prediction["width"], prediction["height"]
    x1, y1 = x - (width/2), y - (height/2)
    x2, y2 = x + (width/2), y + (height/2)
    return (x1, y1, x2, y2)

source_folder = "Volt"
output_folder = "VoltChopped"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through images
for i, filename in enumerate(os.listdir(source_folder)):
    image_path = os.path.join(source_folder, filename)
    
    # Get bounding box coordinates
    bounding_box = get_bounding_box(image_path)
    
    # Crop image
    with Image.open(image_path) as img:
        cropped_img = img.crop(bounding_box)
        output_path = os.path.join(output_folder, filename)
        cropped_img.save(output_path)
