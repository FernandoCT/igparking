import cv2
import numpy as np
import requests
import time
import subprocess

# Updates the parking status by web service
def updateStatusService(numberOfPlaces):

    try:
        serviceURL = "http://igparking.meteor.com/updatestatus/" + str(numberOfPlaces)
        response = requests.get(serviceURL)
        return True
    except requests.ConnectionError, e:
        return False


# Returns True if the spot is free
def isSpotFree(spotTag, spot, emptyImage, currentImage, outputPath):

    y1 = spot[0]
    y2 = spot[1]
    x1 = spot[2]
    x2 = spot[3]

    emptySpot = emptyImage[y1:y2,x1:x2]
    currentSpot = currentImage[y1:y2,x1:x2]
    w, h = currentSpot.shape[::-1]

    res = cv2.matchTemplate(currentSpot,emptySpot,cv2.TM_SQDIFF_NORMED)
    print("res" + str(res))

    threshold = 0.4
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(currentSpot, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    cv2.imwrite(outputPath + "/" + spotTag + "_empty.png", emptySpot)
    cv2.imwrite(outputPath + "/" + spotTag + "_current.png", currentSpot)

    return res < threshold

# Check if the last image taken has available spots
def checkAvailableSpots():

    empty =  cv2.imread("input/empty.jpeg", 0)
    current =  cv2.imread("input/img.jpeg", 0)

    # Camera image is 928x576
    spot1 = [415, 495, 345, 485]
    spot2 = [367,427,400,532]
    spot3 = [400, 480, 70, 150]
    spot4 = [380,421,280,343]

    spots = [spot1, spot2, spot3, spot4]
    freeSpots = [0, 0, 0, 0]

    for (i, spot) in enumerate(spots):
        spotTag = "spot_" + str(i+1)
        isFree = isSpotFree(spotTag, spot, empty, current, "output")
        if isFree:
            freeSpots[i] = 1
            print(spotTag + " is free")
        else:
            freeSpots[i] = 0
            print(spotTag + " is taken")

    freeSpotsCount = sum(freeSpots)
    print("Free spots count: " + str(freeSpotsCount))
    serviceCallOk = updateStatusService(freeSpotsCount)
    print("Invocation service status: " + str(serviceCallOk))


# Starts shell file that takes picture of the parking every minute
def takeCurrentPicture():
    subprocess.call(['./get_parking_image.sh'])


#####
# Main #
#takeCurrentPicture()
while True:
        checkAvailableSpots()
        # Sleep for a minute
        time.sleep(60)
