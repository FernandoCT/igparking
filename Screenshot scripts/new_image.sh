#!/bin/sh
export DATE=`date +%d`
export MONT=`date +%m`
export YEAR=`date +%Y`
mkdir -p /Users/matiasbzurovski/Desktop/Parking/$YEAR/$MONT/$DATE

# Saves screenshot every minute, and saves it as a new image
ffmpeg -i "rtsp://10.15.0.65:554/user=admin&password=&channel=2&stream=0.sdp" -f image2 -vsync 2 -r 1/60 /Users/matiasbzurovski/Desktop/Parking/$YEAR/$MONT/$DATE/img%6d.jpeg
