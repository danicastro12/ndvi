from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from track import track

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

g = camera.awb_gains
camera.awb_mode = "off"
print(g)
camera.awb_gains = (1.4, 0.6)
time.sleep(0.1)

def NDVICalc(original):
	ndvi_img = np.zeros((original.shape[0], original.shape[1], 3), np.uint8)

	red = original[:, :, 2]
	blue = original[:, :, 0]

	center_dx = 30
	center_dy = 30
	red_c = original[(240 - center_dy):(240 + center_dy), (320 - center_dx):(320 + center_dx), 2]
	blue_c = original[(240 - center_dy):(240 + center_dy), (320 - center_dx):(320 + center_dx), 0]

	sum_c = red_c + blue_c
	sum_c[sum_c < 5] = 5
	ndvi_c = (((red_c - blue_c) / sum_c + 1) * 127).astype('uint8')
	ndvi_a = ndvi_c.ravel()
	promedio = np.mean(ndvi_a,dtype=np.float32)

	sum = red + blue
	sum[sum < 5] = 5
	ndvi = (((red -blue) / sum + 1) * 127).astype('uint8')

	cv2.putText(original,f"NDVI:{(promedio / 127) - 1}",(5,30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
	redSat = (ndvi-128) * 2
	bluSat = ((255-ndvi) - 128) * 2

	redSat[ndvi < 128] = 0
	bluSat[ndvi >= 128] = 0

	ndvi_img[:, :, 0] = bluSat
	ndvi_img[:, :, 1] = redSat
	ndvi_img[:, :, 2] = 0

	#colormap = cv2.applyColorMap(ndvi, cv2.COLORMAP_JET)

	return ndvi_img

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	image = frame.array
	ndvi = NDVICalc(image)
	cv2.rectangle(ndvi,(320 - 30, 240 + 30),(320 + 30, 240 - 30), (255,255,255), 2)
	cv2.imshow("orig", image)
	cv2.imshow("Frame", ndvi)
	rawCapture.truncate(0)

	if cv2.waitKey(1) == 27:
		break
