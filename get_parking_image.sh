#!/bin/sh

# Saves screenshot every minute, and replace the previous image
ffmpeg -i "rtsp://10.15.0.65:554/user=admin&password=&channel=2&stream=0.sdp" -f image2 -vsync 2 -updatefirst 1 -r 1/60 input/img.jpeg
