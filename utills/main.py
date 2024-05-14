import select_ROI
import testing


if __name__ == '__main__':

    #get path to the video source
    path = input("Path/link to video: ")

    # get the points for the roi for the selected video source
    ROI_Points = select_ROI.getCoordinates(path)
    print(ROI_Points)

    # get the capacity of the parking from user
    capacity = int(input("Capacity of the parking: "))

    # run the model function on it and calculate the number of cars and print availabe parking space
    testing.getAvailableSpace(path, ROI_Points, capacity)



