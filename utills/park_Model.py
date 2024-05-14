import cv2
import numpy as np
import torch

def getAvailableSpace(video_path, ROI_coordinates, total_capacity):
  """
  Analyzes a video to determine available parking spaces within a designated ROI.

  Args:
      video_path (str): Path to the video file.
      ROI_coordinates (list): List of tuples representing the ROI polygon vertices (x, y).
      total_capacity (int): Total number of parking spaces in the ROI.

  Returns:
      None
  """

  # Load the YOLOv5 model
  model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

  # Open the video capture
  cap = cv2.VideoCapture(video_path)

  # Convert ROI coordinates to NumPy array
  area = np.array(ROI_coordinates, np.int32)

  while True:
    ret, frame = cap.read()

    if not ret:
      break

    # Resize frame for better performance 
    frame = cv2.resize(frame, (1020, 600))

    # Perform object detection using YOLOv5
    results = model(frame)
    cars = []

    # Extract bounding boxes and labels for cars
    for index, row in results.pandas().xyxy[0].iterrows():
      x1 = int(row['xmin'])
      y1 = int(row['ymin'])
      x2 = int(row['xmax'])
      y2 = int(row['ymax'])
      label = str(row['name'])

      if label == 'car':
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # Check if car is within the ROI
        results = cv2.pointPolygonTest(area, (cx, cy), False)
        if results >= 0:
          cars.append([x1, y1, x2, y2])

    # Calculate remaining spaces
    available_spaces = total_capacity - len(cars)

    # Print car count and available spaces to console
    return [available_spaces, int((available_spaces/total_capacity)*100)]

    
    
    
  cap.release()
  cv2.destroyAllWindows()
