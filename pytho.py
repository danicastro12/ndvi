import cv2
from matplotlib import pyplot as plt
import numpy as np

# Cargar la imagen
imagen = cv2.imread('images/captura.jpg')

# Verificar si la imagen se ha cargado correctamente
if imagen is None:
    raise FileNotFoundError("No se pudo cargar la imagen. Verifica la ruta del archivo.")

# Colores
colores = ('b', 'g', 'r')
nombres_colores = ('Azul', 'Verde', 'Rojo')

# Crear una figura para el histograma
plt.figure()
plt.title("Histogramas de colores de la imagen")
plt.xlabel("Intensidad de píxel")
plt.ylabel("Número de píxeles")

# Calcular y graficar los histogramas para cada canal de color
histogramas = []
bins = np.arange(256)
for i, color in enumerate(colores):
    hist = cv2.calcHist([imagen], [i], None, [256], [0, 256]).flatten()
    plt.bar(bins, hist, color=color, alpha=0.5, label=nombres_colores[i])
    histogramas.append(hist)

# Mostrar la leyenda y el grid
plt.legend(loc='upper right')
plt.grid()
plt.show()

# Determinar cuál color predomina
total_pixeles = [sum(hist) for hist in histogramas]
color_predominante = nombres_colores[total_pixeles.index(max(total_pixeles))]
print(f"El color predominante en la imagen es: {color_predominante}")
