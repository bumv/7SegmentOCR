import cv2
import os

def save_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Initialize a counter for frame numbers
    frame_count = 0
    
    while True:
        # Read a frame
        ret, frame = cap.read()
        
        # If we've reached the end of the video, break out of the loop
        if not ret:
            break
        
        if frame_count % 30 == 0:
                
            # Define the path to save the frame
            frame_path = os.path.join(output_folder, f'{frame_count:04d}.jpg')
            
            # Save the frame as an image
            cv2.imwrite(frame_path, frame)
        
        # Increment the frame counter
        frame_count += 1
    
    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()

# Usage
video_path = 'PhysVid2.mp4'  # Replace with the actual path of your video
output_folder = 'Frames/'  # Choose the folder where frames will be saved

save_frames(video_path, output_folder)