import cv2 as cv
import numpy as np
import os

def openImage(path):
    image = cv.imread(path)
    
    if image is None: 
        print("Erro: Não foi possível carregar a imagem.")
    
    return image

# pre processamento das imagens
def preProcessing(image):

    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 
    
    # aplicando um filtro gaussiano de kernel size x size na imagem
    size = 25
    blur = cv.GaussianBlur(image_gray, (size,size), 0)
    
    # aplicando threshold na imagem 
    limiar = 130
    _, image_b = cv.threshold(blur, limiar, 255, cv.THRESH_BINARY)
    
    return image_b

# funcao que mostra as principais estrelas detectadas
def showImage(image_binaria, image_original):
    # encontrar contornos das estrelas
    contours, _ = cv.findContours(image_binaria, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # inicializar uma lista para armazenar as coordenadas dos pontos de interesse
    keypoints = []

    # adiciona os pontos de interesse dos contornos na lista
    for contour in contours:
        M = cv.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            keypoints.append((cX, cY))

    # printa a coordenada das estrelas detectadas
    print("Coordenadas das principais estrelas identificadas:\n")
    for kp in keypoints:
        cv.circle(image_original, kp, 8, (0, 0, 255), -1)
        print(kp)
    
    cv.imshow("Principais Estrelas detectadas", image_original)
    cv.waitKey(0) #espera pressionar qualquer tecla
    cv.destroyAllWindows()

# main program
if __name__ == '__main__':
    
    path0 = os.path.join('..', 'Fotos_stellarium', 'Fotos', 'Triangulum Australe.png')
    path1 = "test1.jpeg"
    
    image = openImage(path0)
    
    showImage(preProcessing(image), image)