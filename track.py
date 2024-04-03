import cv2 as cv
import numpy as np

def nada ():
    pass

cv.namedWindow("Parametros")
cv.createTrackbar("Tonalidad Minima", "Parametros" ,0 , 179, nada)
cv.createTrackbar("Tonalidad Maxima", "Parametros" ,0 , 179, nada)
cv.createTrackbar("Saturacion Minima", "Parametros" ,0 , 255, nada)
cv.createTrackbar("Saturacion Maxima", "Parametros" ,0 , 255, nada)
cv.createTrackbar("Brillo Minima", "Parametros" ,0 , 255, nada)
cv.createTrackbar("Brillo Maxima", "Parametros" ,0 , 255, nada)
cv.createTrackbar("Kernel X", "Parametros" ,1 , 30, nada)
cv.createTrackbar("Kernel Y", "Parametros" ,1 , 30, nada)

video = cv.VideoCapture(0)

while(True):
    ret, frame = video.read()

    if ret:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        tmin = cv.getTrackbarPos("Tonalidad Minima", "Parametros")
        tmax = cv.getTrackbarPos("Tonalidad Maxima", "Parametros")
        smin = cv.getTrackbarPos("Saturacion Minima", "Parametros")
        smax = cv.getTrackbarPos("Saturacion Maxima", "Parametros")
        bmin = cv.getTrackbarPos("Brillo Minima", "Parametros")
        bmax = cv.getTrackbarPos("Brillo Maxima", "Parametros")

        low_color = np.array([tmin, smin, bmin])
        high_color = np.array([tmax, smax, bmax])

        mask = cv.inRange(hsv, low_color, high_color)

        kernelx = cv.getTrackbarPos("Kernel X", "Parametros")
        kernely = cv.getTrackbarPos("Kernel Y", "Parametros")

        kernel = np.ones((kernelx, kernely), np.uint8)

        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

        cv.imshow("Mascara", mask)

        if cv.waitKey(1) == 0xFF & ord('s'):
            break

video.release()
cv.destroyAllWindows()
