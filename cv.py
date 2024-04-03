import cv2 as cv

image = cv.VideoCapture(0)

def NDVICalc(original):
    limit = 5

    red = original[:, :, 2].astype('float')
    blue = original[:, :, 0].astype('float')

    sum = red + blue
    sum[sum < limit] = limit

    ndvi=(((red + blue) / (sum) + 1) * 127).astype('uint8')

    colormap = cv.applyColorMap(ndvi, cv.COLORMAP_JET)

    return colormap

while True:
    ret, frame = image.read()

    ndvi = NDVICalc(frame)
    cv.imshow('CAMARA', ndvi)
    if cv.waitKey(1) & 0xFF == ord('s'):
        break

image.release()
cv.destroyAllWindows()