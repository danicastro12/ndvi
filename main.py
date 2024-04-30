from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

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

	promedio = np.mean(ndvi_a, dtype=np.float32)

	sum = red + blue
	sum[sum < 5] = 5
	ndvi = ((( (red - blue)) / (sum) + 1) * 127).astype('uint8')

	ndvi_prom = f"NDVI:{(promedio / 127) - 1}"
	redSat = (ndvi-128) * 2
	bluSat = ((255-ndvi) - 128) * 2

	redSat[ndvi < 128] = 0
	bluSat[ndvi >= 128] = 0

	ndvi_img[:, :, 0] = bluSat
	ndvi_img[:, :, 1] = redSat
	ndvi_img[:, :, 2] = 0

        #colormap = cv2.applyColorMap(ndvi, cv2.COLORMAP_JET)

	return ndvi_img, ndvi_prom, redSat

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	#Daniel el virgo

	#Obtenemos la imagen y la volteamos para mayor comodidad al procesarla
	#We get the image and flip it for a better comfort to process it
	image = frame.array
	flipped = cv2.flip(image,-1)
	ndvi, prom, redSat = NDVICalc(flipped)

	#Mostramos un rectangulo en el video dentro del cual se toman los valores del ndvi dentro de el mismo
	#We show a rectangle in the video wich takes the ndvi values
	cv2.rectangle(ndvi,(320 - 30, 240 + 30),(320 + 30, 240 - 30), (255,255,255), 2)
	cv2.putText(ndvi, prom, (5,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

	#Tomamos la imagen en escala de grises para aplicarle un umbral y facilitar la busqueda de los contornos de la planta para el tracking
	#We get the image in grayscale to apply a treshold and make easier the search of plants contours
	kernel = np.ones((3,3), np.uint8)
	ret,mask = cv2.threshold(redSat,251,255,cv2.THRESH_BINARY)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	contours, x = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#Filtramos el area del contorno
	#We filter the contour area
	for contour in contours:
		area = cv2.contourArea(contour)
		if area > 7000:
			x, y, w, h = cv2.boundingRect(contour)
			cv2.rectangle(ndvi, (x, y), (x+w, y+h), (0, 255, 0), 3)
			cv2.rectangle(flipped, (x, y), (x+w, y+h), (0, 255, 0), 3)
	cv2.imshow("Frame", ndvi)
	cv2.imshow("mask", mask)
	cv2.imshow("orig", flipped)
	rawCapture.truncate(0)

	if cv2.waitKey(1) == 27:
		break


