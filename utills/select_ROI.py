import cv2
import numpy as np


def getCoordinates(video_path):
  """
  This function takes a video path as input, displays the video, tracks mouse clicks,
  stores click coordinates in a list named 'points', and returns the list on 'q' press.

  Args:
      video_path (str): The path to the video file.

  Returns:
      list: The list of click coordinates stored during video playback.
  """

  # Local list to store click coordinates within the function
  points = []

  # Open the video capture object
  cap = cv2.VideoCapture(video_path)

  # Check if video opened successfully
  if not cap.isOpened():
      print("Error opening video file")
      return points  # Return empty list on error

  # Create a window named 'FRAME' for displaying the video
  cv2.namedWindow('FRAME')


  def on_mouse_click(event, x, y, flags, param):
      """
      Callback function for mouse events. Stores click coordinates in 'points' list.

      Args:
          event (int): The type of mouse event (e.g., cv2.EVENT_LBUTTONDOWN).
          x (int): The x-coordinate of the mouse click.
          y (int): The y-coordinate of the mouse click.
          flags (int): Any flags associated with the event.
          param: Any additional parameters passed to the callback function.
      """
      if event == cv2.EVENT_LBUTTONDOWN:  # Check for left mouse button click
          points.append((x, y))
          print(f"Click coordinates: ({x}, {y}) stored in 'points' list.")

  # Set the mouse callback function for the 'FRAME' window
  cv2.setMouseCallback('FRAME', on_mouse_click)

  while True:
      # Read a frame from the video capture
      ret, frame = cap.read()

      # Check if the frame was read successfully
      if not ret:
          break
      
      frame=cv2.resize(frame,(1020,600))

      # Font and text placement for hover coordinates and instructions
      font = cv2.FONT_HERSHEY_SIMPLEX
      font_scale = 0.6
      text_thickness = 1
      instructions_pos = (550, 503)  # Bottom left corner for instructions

     
      # Draw instructions text
      cv2.putText(frame, "1. Click to add coordinate", instructions_pos, font, font_scale,
                  (255, 255, 255), text_thickness)
      cv2.putText(frame, "2. Press 'backspace' to remove the last click", (instructions_pos[0], instructions_pos[1] + 20), font, font_scale,
                  (255, 255, 255), text_thickness)
      cv2.putText(frame, "3. Press 'enter' to save", (instructions_pos[0], instructions_pos[1] + 40),
                  font, font_scale, (255, 255, 255), text_thickness)
      


      # Display the frame
      cv2.imshow("FRAME", frame)

      # Get a character key press
      key = cv2.waitKey(1) & 0xFF

      # Exit if 'enter' key is pressed
      if key == 13:
          break

    
      # Delete last element if 'backspace' is pressed and there are elements
      if key == 8 and points:
          deleted_coord = points.pop()
          print(f"Deleted last click coordinates: ({deleted_coord[0]}, {deleted_coord[1]})")

  # Release video capture and close all windows
  cap.release()
  cv2.destroyAllWindows()

  # Return the stored click coordinates
  return points