from SimpleCV import Image

# Returns difference between images
def imageDiff(imgA, imgB):
	return (imgA - imgB) + (imgB - imgA)

# Returns True if the spot is free
def isSpotFree(spotTag, spot, emptyImage, currentImage, imageDiffFunc, outputPath):
	emptySpot = emptyImage.crop(spot)
	currentSpot = currentImage.crop(spot)
	diff = imageDiffFunc(emptySpot, currentSpot)
	emptySpot.save(outputPath + "/" + spotTag + "_empty.png")
	currentSpot.save(outputPath + "/" + spotTag + "_current.png")
	diff.save(outputPath + "/" + spotTag + "_diff.png")
	mean = diff.meanColor()
	print(mean)
	threshold_R = 30
	threshold_G = 30
	threshold_B = 30
	isFree = mean[0] < threshold_R and mean[1] < threshold_G and mean[2] < threshold_B
	return isFree

########
# Main #

empty = Image("lot_0.png")
current = Image("lot_1.png")

# Camera image is 928x576
spot1 = [345, 415, 140, 80]
spot2 = [446, 300, 110, 70]
spot3 = [70, 400, 150, 50]
spot4 = [190, 300, 195, 60]

spots = [spot1, spot2, spot3, spot4]
freeSpots = [0, 0, 0, 0]

for (i, spot) in enumerate(spots):
	spotTag = "spot_" + str(i+1)
	isFree = isSpotFree(spotTag, spot, empty, current, imageDiff, "output")
	if isFree:
		freeSpots[i] = 1
		print(spotTag + " is free")
	else:
		freeSpots[i] = 0
		print(spotTag + " is taken")

freeSpotsCount = sum(freeSpots)
print("Free spots count: " + str(freeSpotsCount))