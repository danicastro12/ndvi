#lineal
import cv2
from matplotlib import pyplot as plt

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
for i, color in enumerate(colores):
    hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
    plt.plot(hist, color=color)
    histogramas.append(hist)
    plt.xlim([0, 256])

# Mostrar la leyenda y el grid
plt.legend(nombres_colores)
plt.grid()
plt.show()

# Determinar cuál color predomina
total_pixeles = [sum(hist) for hist in histogramas]
color_predominante = nombres_colores[total_pixeles.index(max(total_pixeles))]
print(f"El color predominante en la imagen es: {color_predominante}")
