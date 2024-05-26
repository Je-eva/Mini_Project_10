import os
import cv2
import easyocr
import numpy as np

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Path to the folder containing images for training
training_folder_path = 'C:/Users/JESWIN/OneDrive/Documents/python/opencv projects/myvenv/Scripts/proj/Images'

# Path to the folder containing images with access number plates
access_folder_path = 'C:/Users/JESWIN/OneDrive/Documents/python/opencv projects/myvenv/Scripts/proj/Images'

# Create an EasyOCR reader object
reader = easyocr.Reader(['en'], gpu=True)

# Function to train and understand license plates from images
def train_and_understand():
    # Get a list of all files in the training folder
    training_files = os.listdir(training_folder_path)

    # Iterate through each image file in the training folder
    for file in training_files:
        image_path = os.path.join(training_folder_path, file)
        
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        
        # Convert the image to a NumPy array
        image_np = np.array(image)

        # Perform OCR on the image
        results = reader.readtext(image_np)

        # Print the extracted text
        for result in results:
            print(f"License plate text from {file}: {result[1]}")

# Function to compare text from captured image with texts from images in the access folder
def check_access(text):
    access_files = os.listdir(access_folder_path)
    for file in access_files:
        image_path = os.path.join(access_folder_path, file)
        image = cv2.imread(image_path)
        image_np = np.array(image)
        results = reader.readtext(image_np)
        for result in results:
            if text == result[1]:
                return True
    return False

# Function to capture video from camera and check access
def capture_video_and_check_access():
    # Initialize camera
    camera = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        # Convert frame to a NumPy array
        frame_np = np.array(frame)

        # Perform OCR on the captured frame
        results = reader.readtext(frame_np)

        # Extract text from OCR results
        extracted_text = [result[1] for result in results]

        # Check if extracted text matches with any of the texts in access folder
        for text in extracted_text:
            if check_access(text):
                print("Access granted.")
                camera.release()
                return
            else:
                print("Access denied. Sending email notification.")
                # send_email() # Implement email notification
                camera.release()
                return

        # Display the captured frame
        cv2.imshow('Live Video Feed', frame)

        # Check for 'q' key press to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera
    camera.release()
    cv2.destroyAllWindows()

# Main function
def main():
    # Train and understand license plates from images in the training folder
    train_and_understand()

    # Capture video from camera and check access
    capture_video_and_check_access()

if __name__ == "__main__":
    main()
 
